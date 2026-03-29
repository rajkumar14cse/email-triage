from typing import Any, Dict, List
from env.models import Action, EmailItem, Observation, Reward
from data.emails import EMAILS

TASK_ID = "task_medium_triage"
TASK_DESCRIPTION = "Triage each email: (1) classify category, (2) assign priority (urgent/high/medium/low), (3) route to department (billing/support/legal/hr/sales/management/ignore)."
CATEGORIES = ["billing", "technical", "complaint", "inquiry", "spam", "hr", "legal", "other"]
PRIORITIES = ["urgent", "high", "medium", "low"]
DEPARTMENTS = ["billing", "support", "legal", "hr", "sales", "management", "ignore"]
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
        context={"categories": CATEGORIES, "priorities": PRIORITIES, "departments": DEPARTMENTS},
        available_actions=["prioritize", "skip"],
    )


def grade_action(action: Action) -> Reward:
    email_id = action.email_id
    ground = next((e for e in EMAILS if e["id"] == email_id), None)
    if ground is None:
        return Reward(total=0.0, message=f"Unknown email id: {email_id}", penalty=-0.1)
    if action.action_type == "skip":
        return Reward(total=0.0, message="Skipped.")
    if action.action_type != "prioritize":
        return Reward(total=0.0, message="Use action_type='prioritize'.", penalty=-0.05)

    gt = ground["ground_truth"]
    feedback = []

    cat_score = 0.0
    if action.classification:
        pred = action.classification.lower().strip()
        if pred == gt["category"]: cat_score = 1.0; feedback.append(f"Category ✓")
        elif pred in CATEGORIES: cat_score = 0.3; feedback.append(f"Category partial")
        else: feedback.append(f"Category invalid")
    else:
        feedback.append("Category missing")

    pri_score = 0.0
    if action.priority:
        pred = action.priority.lower().strip()
        if pred == gt["priority"]: pri_score = 1.0; feedback.append("Priority ✓")
        elif pred in PRIORITIES:
            order = ["urgent", "high", "medium", "low"]
            diff = abs(order.index(pred) - order.index(gt["priority"])) if pred in order else 2
            pri_score = 0.5 if diff == 1 else 0.0
            feedback.append(f"Priority partial")
        else: feedback.append("Priority invalid")
    else:
        feedback.append("Priority missing")

    rte_score = 0.0
    adj = {"billing": ["support"], "support": ["billing", "management"], "legal": ["management", "hr"], "hr": ["legal"], "sales": ["management"], "management": ["support"], "ignore": []}
    if action.routing_department:
        pred = action.routing_department.lower().strip()
        if pred == gt["routing_department"]: rte_score = 1.0; feedback.append("Routing ✓")
        elif pred in DEPARTMENTS:
            rte_score = 0.3 if pred in adj.get(gt["routing_department"], []) else 0.0
            feedback.append(f"Routing partial")
        else: feedback.append("Routing invalid")
    else:
        feedback.append("Routing missing")

    total = round(cat_score * 0.30 + pri_score * 0.35 + rte_score * 0.35, 4)
    return Reward(total=total, classification_score=cat_score, priority_score=pri_score, routing_score=rte_score, message=" | ".join(feedback))


def compute_episode_score(rewards: List[float]) -> Dict[str, Any]:
    if not rewards:
        return {"score": 0.0, "total_emails": 0}
    return {"score": round(sum(rewards) / len(rewards), 4), "total_emails": len(rewards)}