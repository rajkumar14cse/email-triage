from typing import Any, Dict, List
from env.models import Action, EmailItem, Observation, Reward
from data.emails import EMAILS, RESPONSE_TEMPLATES

TASK_ID = "task_hard_full_triage"
TASK_DESCRIPTION = "Full triage: classify, prioritize, route, AND draft a professional response. For spam/newsletters use action_type='archive'. For all others use action_type='respond' with response_draft filled."
CATEGORIES = ["billing", "technical", "complaint", "inquiry", "spam", "hr", "legal", "other"]
PRIORITIES = ["urgent", "high", "medium", "low"]
DEPARTMENTS = ["billing", "support", "legal", "hr", "sales", "management", "ignore"]
MAX_STEPS = len(EMAILS)
NO_RESPONSE_IDS = {"e005", "e009"}


def get_emails() -> List[EmailItem]:
    return [EmailItem(id=e["id"], subject=e["subject"], sender=e["sender"], body=e["body"], timestamp=e["timestamp"]) for e in EMAILS]


def build_observation(emails: List[EmailItem], step: int, processed_ids: List[str]) -> Observation:
    remaining = [e for e in emails if e.id not in processed_ids]
    return Observation(
        task_id=TASK_ID,
        task_description=TASK_DESCRIPTION,
        emails=remaining[:2],
        inbox_size=len(remaining),
        step_number=step,
        max_steps=MAX_STEPS,
        context={"categories": CATEGORIES, "priorities": PRIORITIES, "departments": DEPARTMENTS, "no_response_needed_for": ["spam", "other"]},
        available_actions=["respond", "archive", "flag"],
    )


def grade_action(action: Action) -> Reward:
    email_id = action.email_id
    ground = next((e for e in EMAILS if e["id"] == email_id), None)
    if ground is None:
        return Reward(total=0.0, message=f"Unknown email id: {email_id}", penalty=-0.1)

    gt = ground["ground_truth"]
    template = RESPONSE_TEMPLATES.get(email_id, {})
    feedback = []
    penalty = 0.0
    is_no_response = email_id in NO_RESPONSE_IDS

    if is_no_response:
        action_ok = 1.0 if action.action_type == "archive" else 0.0
        if action_ok == 0.0:
            penalty -= 0.1
            feedback.append("Should archive spam")
        else:
            feedback.append("Action ✓ archived")
    else:
        action_ok = 1.0 if action.action_type in ("respond", "flag") else 0.0
        if action.action_type == "archive":
            penalty -= 0.15
            feedback.append("Should NOT archive this email")

    cat_score = 0.0
    if action.classification:
        pred = action.classification.lower().strip()
        if pred == gt["category"]: cat_score = 1.0; feedback.append("Category ✓")
        elif pred in CATEGORIES: cat_score = 0.3; feedback.append("Category partial")
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
            feedback.append("Priority partial")

    rte_score = 0.0
    if action.routing_department:
        pred = action.routing_department.lower().strip()
        if pred == gt["routing_department"]: rte_score = 1.0; feedback.append("Routing ✓")
        elif pred in DEPARTMENTS: rte_score = 0.3; feedback.append("Routing partial")

    if is_no_response:
        resp_score = action_ok
    elif action.response_draft:
        resp_score = _grade_response(action.response_draft, template, feedback)
    else:
        resp_score = 0.0
        penalty -= 0.1
        feedback.append("Response missing")

    total = max(0.0, min(1.0, round(cat_score * 0.20 + pri_score * 0.25 + rte_score * 0.25 + resp_score * 0.30 + penalty, 4)))
    return Reward(total=total, classification_score=cat_score, priority_score=pri_score, routing_score=rte_score, response_score=resp_score, penalty=penalty, message=" | ".join(feedback))


def _grade_response(draft: str, template: Dict[str, Any], feedback: List[str]) -> float:
    score = 0.0
    dl = draft.lower()
    must = template.get("must_include", [])
    if must:
        found = sum(1 for kw in must if kw.lower() in dl)
        score += (found / len(must)) * 0.4
        feedback.append(f"Keywords {found}/{len(must)}")
    else:
        score += 0.4
    wc = len(draft.split())
    if wc >= 80: score += 0.2
    elif wc >= 40: score += 0.1
    if template.get("should_acknowledge", False):
        acks = ["thank you", "we understand", "i understand", "i apologize", "sorry to hear", "received your", "we apologize"]
        if any(p in dl for p in acks): score += 0.2
        else: feedback.append("Missing acknowledgement")
    if template.get("escalation_needed", False):
        escs = ["escalat", "senior", "team", "priorit", "immediately", "urgent", "investigate"]
        if any(p in dl for p in escs): score += 0.2
        else: feedback.append("Missing escalation signal")
    else:
        score += 0.2
    return min(1.0, score)


def compute_episode_score(rewards: List[float]) -> Dict[str, Any]:
    if not rewards:
        return {"score": 0.0, "total_emails": 0}
    return {"score": round(sum(rewards) / len(rewards), 4), "total_emails": len(rewards)}