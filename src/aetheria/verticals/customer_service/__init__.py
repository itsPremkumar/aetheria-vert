"""Customer Service Vertical Plugin."""
from __future__ import annotations
from ..core import VerticalPlugin


class CustomerServicePlugin(VerticalPlugin):
    """Customer Service domain plugin."""

    def __init__(self) -> None:
        super().__init__("customer_service", "Customer Service domain — tickets, issues, resolutions, channels")
        self.register_pattern("issue", [
            r"\b(complaint|inquiry|request|feedback|escalation|refund|return|exchange)\b",
            r"\b(technical issue|billing issue|shipping issue|product issue|service issue)\b",
        ])
        self.register_pattern("channel", [
            r"\b(email|phone|chat|social media|self-service|in-app|video call)\b",
            r"\b(FAQ|knowledge base|community forum|chatbot|virtual agent)\b",
        ])
        self.register_pattern("sentiment", [
            r"\b(satisfied|dissatisfied|frustrated|happy|angry|neutral|delighted|confused)\b",
        ])
        self.register_pattern("resolution", [
            r"\b(resolved|unresolved|pending|closed|reopened|escalated|transferred)\b",
        ])
        self.register_pattern("agent", [
            r"\b(support agent|supervisor|manager|team lead|specialist|representative)\b",
        ])
        self.register_relation("issue", "handled_via", "channel")
        self.register_relation("agent", "resolves", "issue")
        self.register_relation("resolution", "applies_to", "issue")

    def reason(self, entities: list, query: str) -> str:
        issues = [e for e in entities if e.entity_type == "issue"]
        channels = [e for e in entities if e.entity_type == "channel"]
        resolutions = [e for e in entities if e.entity_type == "resolution"]
        parts = []
        if issues:
            parts.append(f"Issue types: {', '.join(i.name for i in issues)}")
        if channels:
            parts.append(f"Service channels: {', '.join(c.name for c in channels)}")
        if resolutions:
            parts.append(f"Resolution status: {', '.join(r.name for r in resolutions)}")
        if not parts:
            return "No specific customer service entities identified."
        return ". ".join(parts) + "."
