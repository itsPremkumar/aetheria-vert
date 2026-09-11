"""Research Vertical Plugin."""
from __future__ import annotations
from ..core import VerticalPlugin


class ResearchPlugin(VerticalPlugin):
    """Research domain plugin."""

    def __init__(self) -> None:
        super().__init__("research", "Research domain — hypotheses, experiments, publications, methods")
        self.register_pattern("hypothesis", [
            r"\b(hypothesis|assumption|prediction|theory|model|framework)\b",
        ])
        self.register_pattern("method", [
            r"\b(experiment|survey|case study|literature review|meta-analysis|simulation)\b",
            r"\b(regression|classification|clustering|natural language processing|deep learning)\b",
        ])
        self.register_pattern("publication", [
            r"\b(journal|conference|preprint|patent|technical report|white paper|dissertation)\b",
            r"\b(article|paper|proceedings|abstract|full text|supplementary material)\b",
        ])
        self.register_pattern("metric", [
            r"\b(accuracy|precision|recall|F1|AUC|ROC|RMSE|MAE|BLEU|ROUGE|METEOR)\b",
            r"\b(p-value|confidence interval|statistical significance|effect size|power)\b",
        ])
        self.register_pattern("domain", [
            r"\b(AI|machine learning|NLP|computer vision|robotics|quantum|biotechnology)\b",
            r"\b(neuroscience|genomics|astrophysics|materials science|climate science)\b",
        ])
        self.register_relation("method", "tests", "hypothesis")
        self.register_relation("publication", "reports", "hypothesis")
        self.register_relation("metric", "measures", "method")

    def reason(self, entities: list, query: str) -> str:
        hypotheses = [e for e in entities if e.entity_type == "hypothesis"]
        methods = [e for e in entities if e.entity_type == "method"]
        publications = [e for e in entities if e.entity_type == "publication"]
        parts = []
        if hypotheses:
            parts.append(f"Hypotheses: {', '.join(h.name for h in hypotheses)}")
        if methods:
            parts.append(f"Methods: {', '.join(m.name for m in methods)}")
        if publications:
            parts.append(f"Publications: {', '.join(p.name for p in publications)}")
        if not parts:
            return "No specific research entities identified."
        return ". ".join(parts) + "."
