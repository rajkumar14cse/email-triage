from typing import Any, Dict, List
from env.models import Action, EnvironmentState, Observation, Reward, StepResult
from tasks import task_easy, task_medium, task_hard

TASK_REGISTRY = {
    task_easy.TASK_ID: task_easy,
    task_medium.TASK_ID: task_medium,
    task_hard.TASK_ID: task_hard,
}
DEFAULT_TASK = task_easy.TASK_ID


class EmailTriageEnvironment:
    def __init__(self, task_id: str = DEFAULT_TASK):
        if task_id not in TASK_REGISTRY:
            raise ValueError(f"Unknown task '{task_id}'. Choose from: {list(TASK_REGISTRY.keys())}")
        self._task_id = task_id
        self._task = TASK_REGISTRY[task_id]
        self._step_number = 0
        self._emails = []
        self._processed_ids = []
        self._rewards = []
        self._done = False
        self._total_reward = 0.0

    def reset(self) -> Observation:
        self._step_number = 0
        self._emails = self._task.get_emails()
        self._processed_ids = []
        self._rewards = []
        self._done = False
        self._total_reward = 0.0
        return self._task.build_observation(self._emails, 0, [])

    def step(self, action: Action) -> StepResult:
        if self._done:
            obs = self._task.build_observation(self._emails, self._step_number, self._processed_ids)
            return StepResult(observation=obs, reward=Reward(total=0.0, message="Episode done. Call reset()."), done=True, info={})

        if action.email_id in self._processed_ids:
            obs = self._task.build_observation(self._emails, self._step_number, self._processed_ids)
            self._step_number += 1
            return StepResult(observation=obs, reward=Reward(total=0.0, penalty=-0.05, message="Already processed."), done=False, info={})

        reward = self._task.grade_action(action)
        self._processed_ids.append(action.email_id)
        self._rewards.append(reward.total)
        self._total_reward += reward.total
        self._step_number += 1

        all_processed = len(self._processed_ids) >= len(self._emails)
        max_steps_reached = self._step_number >= self._task.MAX_STEPS
        self._done = all_processed or max_steps_reached

        obs = self._task.build_observation(self._emails, self._step_number, self._processed_ids)
        info: Dict[str, Any] = {
            "emails_processed": len(self._processed_ids),
            "emails_remaining": len(self._emails) - len(self._processed_ids),
            "running_avg_reward": round(self._total_reward / len(self._rewards), 4) if self._rewards else 0.0,
        }
        if self._done:
            episode_score = self._task.compute_episode_score(self._rewards)
            info["episode_score"] = episode_score
            info["final_score"] = episode_score.get("score", 0.0)

        return StepResult(observation=obs, reward=reward, done=self._done, info=info)

    def state(self) -> EnvironmentState:
        return EnvironmentState(
            task_id=self._task_id,
            step_number=self._step_number,
            max_steps=self._task.MAX_STEPS,
            total_reward=round(self._total_reward, 4),
            emails_processed=len(self._processed_ids),
            emails_remaining=len(self._emails) - len(self._processed_ids),
            episode_done=self._done,
            task_scores={"running_avg": round(self._total_reward / len(self._rewards), 4) if self._rewards else 0.0},
        )

    @property
    def task_ids(self) -> List[str]:
        return list(TASK_REGISTRY.keys())