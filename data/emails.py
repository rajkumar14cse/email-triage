from typing import List, Dict, Any

EMAILS: List[Dict[str, Any]] = [
    {
        "id": "e001",
        "subject": "Invoice #INV-2024-0891 overdue - urgent payment required",
        "sender": "accounts@supplierco.com",
        "body": "Dear Finance Team,\n\nThis is a reminder that invoice #INV-2024-0891 for $12,450 was due on 15 November 2024. Payment is now 30 days overdue. Please arrange payment immediately to avoid service interruption.\n\nBest regards,\nAccounts Receivable, SupplierCo",
        "timestamp": "2024-12-15T09:15:00Z",
        "ground_truth": {
            "category": "billing",
            "priority": "urgent",
            "routing_department": "billing",
        },
    },
    {
        "id": "e002",
        "subject": "Cannot login to dashboard - getting 503 error",
        "sender": "john.smith@clientcorp.com",
        "body": "Hi Support,\n\nI've been trying to access my dashboard since this morning and keep getting a 503 Service Unavailable error. I have a board presentation in 2 hours and desperately need access to my reports. Please help ASAP!\n\nAccount: #ACC-45892\nJohn Smith, ClientCorp",
        "timestamp": "2024-12-15T08:30:00Z",
        "ground_truth": {
            "category": "technical",
            "priority": "urgent",
            "routing_department": "support",
        },
    },
    {
        "id": "e003",
        "subject": "Completely unacceptable service - threatening legal action",
        "sender": "angry.customer@email.com",
        "body": "I am absolutely furious with your service. My order (#ORD-78321) has been delayed for 3 weeks with no communication. I have lost business because of your incompetence. If I do not receive a full refund and compensation within 48 hours, I will be contacting my solicitor and filing a complaint with the consumer ombudsman.\n\nMr. Robert Chen",
        "timestamp": "2024-12-15T10:45:00Z",
        "ground_truth": {
            "category": "complaint",
            "priority": "urgent",
            "routing_department": "legal",
        },
    },
    {
        "id": "e004",
        "subject": "Question about enterprise pricing tiers",
        "sender": "procurement@bigcorp.com",
        "body": "Hello,\n\nWe are evaluating your platform for deployment across our 500-person engineering team. Could you send us information about enterprise pricing, volume discounts, and SLA guarantees? We are making a decision by end of Q1.\n\nThanks,\nSarah Johnson, Procurement Manager, BigCorp",
        "timestamp": "2024-12-15T11:00:00Z",
        "ground_truth": {
            "category": "inquiry",
            "priority": "high",
            "routing_department": "sales",
        },
    },
    {
        "id": "e005",
        "subject": "Congratulations! You've won a $1000 Amazon gift card!!!",
        "sender": "winner-notifications@prize-claim-now.net",
        "body": "CONGRATULATIONS!! You have been selected as our lucky winner! Click here NOW to claim your $1000 Amazon gift card! Limited time offer! Act fast! Click: http://prize-claim-now.net/claim?id=xk291jd",
        "timestamp": "2024-12-15T07:00:00Z",
        "ground_truth": {
            "category": "spam",
            "priority": "low",
            "routing_department": "ignore",
        },
    },
    {
        "id": "e006",
        "subject": "Request for additional parental leave - policy clarification",
        "sender": "emily.watson@ourcompany.com",
        "body": "Dear HR,\n\nI am expecting my second child in March and would like to understand the extended parental leave options available. The current policy document mentions 'enhanced leave packages' but doesn't detail eligibility. Could we schedule a call this week to discuss my options?\n\nKind regards,\nEmily Watson, Senior Developer",
        "timestamp": "2024-12-15T09:45:00Z",
        "ground_truth": {
            "category": "hr",
            "priority": "medium",
            "routing_department": "hr",
        },
    },
    {
        "id": "e007",
        "subject": "Data processing agreement renewal - GDPR compliance",
        "sender": "legal@partnerorg.eu",
        "body": "Dear Legal Team,\n\nOur Data Processing Agreement expires on 31 January 2025. Under GDPR Article 28, we are required to have an updated DPA in place before this date. I have attached the draft renewal. Please review and return signed by 20 January 2025.\n\nRegards,\nMaria Kowalski, DPO, PartnerOrg EU",
        "timestamp": "2024-12-15T14:00:00Z",
        "ground_truth": {
            "category": "legal",
            "priority": "high",
            "routing_department": "legal",
        },
    },
    {
        "id": "e008",
        "subject": "Server performance degradation - monitoring alert",
        "sender": "monitoring@internal-ops.com",
        "body": "ALERT: Production server cluster-03 is showing elevated response times.\nAverage latency: 2,400ms (threshold: 500ms)\nCPU usage: 94%\nAffected services: API Gateway, Authentication Service\nStarted: 2024-12-15 13:45 UTC\nPlease investigate immediately.",
        "timestamp": "2024-12-15T13:50:00Z",
        "ground_truth": {
            "category": "technical",
            "priority": "urgent",
            "routing_department": "support",
        },
    },
    {
        "id": "e009",
        "subject": "Monthly newsletter - December product updates",
        "sender": "newsletter@techblog.io",
        "body": "Hi there,\n\nHere are this month's highlights: new feature releases, upcoming webinars, and community spotlights. Read more at our blog. To unsubscribe from these emails, click here.\n\nThe TechBlog Team",
        "timestamp": "2024-12-15T08:00:00Z",
        "ground_truth": {
            "category": "other",
            "priority": "low",
            "routing_department": "ignore",
        },
    },
    {
        "id": "e010",
        "subject": "Refund request - duplicate charge on account",
        "sender": "customer.service.query@retailuser.com",
        "body": "Hello,\n\nI noticed I was charged twice for my subscription renewal on December 10th. Both charges of $49.99 appear on my credit card statement. Order reference: ORD-2024-11872. Please refund the duplicate charge.\n\nThank you,\nMichael Torres",
        "timestamp": "2024-12-15T12:30:00Z",
        "ground_truth": {
            "category": "billing",
            "priority": "medium",
            "routing_department": "billing",
        },
    },
]

RESPONSE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "e001": {"must_include": ["invoice", "payment", "billing"], "tone": "professional", "should_acknowledge": True, "escalation_needed": True},
    "e002": {"must_include": ["503", "investigating", "update"], "tone": "urgent_helpful", "should_acknowledge": True, "escalation_needed": True},
    "e003": {"must_include": ["apolog", "refund", "legal", "resolve"], "tone": "de_escalating", "should_acknowledge": True, "escalation_needed": True},
    "e004": {"must_include": ["pricing", "enterprise", "contact", "sales"], "tone": "professional", "should_acknowledge": True, "escalation_needed": False},
    "e005": {"must_include": [], "tone": "none", "should_acknowledge": False, "escalation_needed": False},
    "e006": {"must_include": ["parental", "hr", "policy", "schedule"], "tone": "empathetic", "should_acknowledge": True, "escalation_needed": False},
    "e007": {"must_include": ["dpa", "gdpr", "legal", "review"], "tone": "professional", "should_acknowledge": True, "escalation_needed": True},
    "e008": {"must_include": ["investigating", "latency", "team"], "tone": "urgent_helpful", "should_acknowledge": True, "escalation_needed": True},
    "e009": {"must_include": [], "tone": "none", "should_acknowledge": False, "escalation_needed": False},
    "e010": {"must_include": ["duplicate", "refund", "charge"], "tone": "professional", "should_acknowledge": True, "escalation_needed": False},
}