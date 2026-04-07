from typing import Any, Dict, List
from env.models import Action, EmailItem, Observation, Reward
from data.emails import EMAILS

TASK_ID = "task_easy_classify"
TASK_DESCRIPTION = "Classify each email into one of the following categories: billing, technical, complaint, inquiry, spam, hr, legal, other."
CATEGORIES = ["billing", "technical", "complaint", "inquiry", "spam", "hr", "legal", "other"]
MAX_STEPS = len(EMAILS)


def get_emails() -> List[EmailItem]:
    return [EmailItem(id=e["id"], subject=e["subject"], sender=e["sender"], body=e["body"], timestamp=e["timestamp"]) for e in EMAILS]


def build_observation(emails: List[EmailItem], step: int, processed_ids: List[str]) -> Observation:
    remaining = [e for e in emails if e.id not in processed_ids]
    return Observation(
        task_id=TASK_ID,
        task_description=TASK_DESCRIPTION,
        emails=remaining[:3],
        inbox_size=len(remaining),
        step_number=step,
        max_steps=MAX_STEPS,
        context={"categories": CATEGORIES, "instructions": "Use action_type='classify' and set the 'classification' field."},
        available_actions=["classify", "skip"],
    )


def grade_action(action: Action) -> Reward:
    email_id = action.email_id
    ground = next((e for e in EMAILS if e["id"] == email_id), None)
    if ground is None:
        return Reward(total=0.0, message=f"Unknown email id: {email_id}", penalty=-0.1)
    if action.action_type == "skip":
        return Reward(total=0.0, message="Skipped.")
    if action.action_type != "classify":
        return Reward(total=0.0, message=f"Wrong action type. Use 'classify'.", penalty=-0.05)
    if action.classification is None:
        return Reward(total=0.0, message="No classification provided.", penalty=-0.05)

    correct = ground["ground_truth"]["category"]
    predicted = action.classification.lower().strip()

    if predicted == correct:
        return Reward(total=1.0, classification_score=1.0, message=f"Correct! '{predicted}'")
    elif predicted in CATEGORIES:
        partial = _partial_credit(predicted, correct)
        return Reward(total=partial, classification_score=partial, message=f"Wrong. Got '{predicted}', expected '{correct}'")
    else:
        return Reward(total=0.0, message=f"Invalid category '{predicted}'")


def _partial_credit(predicted: str, correct: str) -> float:
    adjacent = {
        "billing": ["inquiry"], "technical": ["other"], "complaint": ["legal", "billing"],
        "inquiry": ["billing"], "legal": ["complaint", "hr"], "hr": ["legal", "other"],
        "spam": ["other"], "other": ["inquiry"],
    }
    return 0.3 if predicted in adjacent.get(correct, []) else 0.0


def compute_episode_score(rewards: List[float]) -> Dict[str, Any]:
    if not rewards:
        return {"score": 0.0, "emails_correct": 0, "total_emails": 0}
    avg = sum(rewards) / len(rewards)
    correct = sum(1 for r in rewards if r >= 1.0)
    return {"score": round(avg, 4), "emails_correct": correct, "total_emails": len(rewards)}