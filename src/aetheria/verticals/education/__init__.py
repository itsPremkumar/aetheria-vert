"""Education Vertical Plugin."""
from __future__ import annotations
from ..core import VerticalPlugin


class EducationPlugin(VerticalPlugin):
    """Education domain plugin."""

    def __init__(self) -> None:
        super().__init__("education", "Education domain — subjects, skills, learning paths, assessments")
        self.register_pattern("subject", [
            r"\b(mathematics|science|history|geography|literature|philosophy|psychology)\b",
            r"\b(computer science|engineering|medicine|law|business|economics|art|music)\b",
        ])
        self.register_pattern("skill", [
            r"\b(critical thinking|problem solving|communication|collaboration|creativity)\b",
            r"\b(programming|data analysis|research writing|public speaking|leadership)\b",
        ])
        self.register_pattern("learning_method", [
            r"\b(lecture|seminar|workshop|tutorial|lab|project-based|flipped classroom)\b",
            r"\b(e-learning|blended learning|experiential learning|peer learning|mentorship)\b",
        ])
        self.register_pattern("assessment", [
            r"\b(exam|quiz|essay|presentation|portfolio|peer review|self-assessment)\b",
            r"\b(formative assessment|summative assessment|standardized test|rubric)\b",
        ])
        self.register_pattern("credential", [
            r"\b(degree|diploma|certificate|badge|micro-credential|license|accreditation)\b",
        ])
        self.register_relation("subject", "requires", "skill")
        self.register_relation("learning_method", "develops", "skill")
        self.register_relation("assessment", "measures", "skill")

    def reason(self, entities: list, query: str) -> str:
        subjects = [e for e in entities if e.entity_type == "subject"]
        skills = [e for e in entities if e.entity_type == "skill"]
        methods = [e for e in entities if e.entity_type == "learning_method"]
        parts = []
        if subjects:
            parts.append(f"Subject areas: {', '.join(s.name for s in subjects)}")
        if skills:
            parts.append(f"Skills: {', '.join(s.name for s in skills)}")
        if methods:
            parts.append(f"Learning methods: {', '.join(m.name for m in methods)}")
        if not parts:
            return "No specific education entities identified."
        return ". ".join(parts) + "."
