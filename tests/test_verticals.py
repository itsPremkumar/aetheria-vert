"""Tests for remaining vertical plugins and benchmark suite."""
from __future__ import annotations

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from aetheria.verticals.legal import LegalPlugin
from aetheria.verticals.finance import FinancePlugin
from aetheria.verticals.education import EducationPlugin
from aetheria.verticals.customer_service import CustomerServicePlugin
from aetheria.verticals.manufacturing import ManufacturingPlugin
from aetheria.verticals.agriculture import AgriculturePlugin
from aetheria.verticals.research import ResearchPlugin
from aetheria.benchmark import BenchmarkSuite, BenchmarkResult


# ─── Legal Plugin Tests ────────────────────────────────────────────────────────

class TestLegalPlugin:
    def test_extract_parties(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("The plaintiff and defendant reached an agreement")
        party_names = [e.name for e in entities if e.entity_type == "party"]
        assert "plaintiff" in party_names
        assert "defendant" in party_names

    def test_extract_clauses(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("The indemnification and termination clauses are included")
        clause_names = [e.name for e in entities if e.entity_type == "clause"]
        assert "indemnification" in clause_names
        assert "termination" in clause_names

    def test_extract_documents(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("The contract and agreement were signed")
        doc_names = [e.name for e in entities if e.entity_type == "document"]
        assert "contract" in doc_names
        assert "agreement" in doc_names

    def test_extract_courts(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("The district court and appeals court ruled")
        court_names = [e.name for e in entities if e.entity_type == "court"]
        assert "district court" in court_names


# ─── Finance Plugin Tests ──────────────────────────────────────────────────────

class TestFinancePlugin:
    def test_extract_assets(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("Invest in stock, bond, and ETF")
        asset_names = [e.name for e in entities if e.entity_type == "asset"]
        assert "stock" in asset_names
        assert "bond" in asset_names

    def test_extract_transactions(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("Buy and sell trades were executed")
        tx_names = [e.name for e in entities if e.entity_type == "transaction"]
        assert "buy" in tx_names or "sell" in tx_names

    def test_extract_regulations(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("Comply with SEC, FINRA, and Basel III")
        reg_names = [e.name for e in entities if e.entity_type == "regulation"]
        assert "sec" in reg_names or "finra" in reg_names

    def test_extract_risks(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("Market risk and credit risk were assessed")
        risk_names = [e.name for e in entities if e.entity_type == "risk"]
        assert "market risk" in risk_names


# ─── Education Plugin Tests ────────────────────────────────────────────────────

class TestEducationPlugin:
    def test_extract_subjects(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("Study mathematics, science, and history")
        subject_names = [e.name for e in entities if e.entity_type == "subject"]
        assert "mathematics" in subject_names
        assert "science" in subject_names

    def test_extract_skills(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("Develop critical thinking and problem solving")
        skill_names = [e.name for e in entities if e.entity_type == "skill"]
        assert "critical thinking" in skill_names

    def test_extract_methods(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("Use lecture, seminar, and workshop")
        method_names = [e.name for e in entities if e.entity_type == "learning_method"]
        assert "lecture" in method_names

    def test_extract_assessments(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("Give exam, quiz, and essay")
        assessment_names = [e.name for e in entities if e.entity_type == "assessment"]
        assert "exam" in assessment_names


# ─── Customer Service Plugin Tests ─────────────────────────────────────────────

class TestCustomerServicePlugin:
    def test_extract_issues(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("The customer has a complaint and inquiry")
        issue_names = [e.name for e in entities if e.entity_type == "issue"]
        assert "complaint" in issue_names
        assert "inquiry" in issue_names

    def test_extract_channels(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("Support via email, phone, and chat")
        channel_names = [e.name for e in entities if e.entity_type == "channel"]
        assert "email" in channel_names
        assert "phone" in channel_names

    def test_extract_resolutions(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("The ticket was resolved and closed")
        resolution_names = [e.name for e in entities if e.entity_type == "resolution"]
        assert "resolved" in resolution_names
        assert "closed" in resolution_names


# ─── Manufacturing Plugin Tests ────────────────────────────────────────────────

class TestManufacturingPlugin:
    def test_extract_processes(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("Assembly and fabrication processes")
        process_names = [e.name for e in entities if e.entity_type == "process"]
        assert "assembly" in process_names
        assert "fabrication" in process_names

    def test_extract_equipment(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("Use CNC, lathe, and mill")
        equipment_names = [e.name for e in entities if e.entity_type == "equipment"]
        assert "cnc" in equipment_names

    def test_extract_quality(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("Follow ISO 9001 and Six Sigma standards")
        quality_names = [e.name for e in entities if e.entity_type == "quality"]
        assert "iso 9001" in quality_names or "six sigma" in quality_names


# ─── Agriculture Plugin Tests ──────────────────────────────────────────────────

class TestAgriculturePlugin:
    def test_extract_crops(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("Grow wheat, corn, and rice")
        crop_names = [e.name for e in entities if e.entity_type == "crop"]
        assert "wheat" in crop_names
        assert "corn" in crop_names

    def test_extract_soils(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("Plant in clay, sandy, and loam soil")
        soil_names = [e.name for e in entities if e.entity_type == "soil"]
        assert "clay" in soil_names
        assert "sandy" in soil_names

    def test_extract_pests(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("Control aphid, caterpillar, and beetle")
        pest_names = [e.name for e in entities if e.entity_type == "pest"]
        assert "aphid" in pest_names
        assert "caterpillar" in pest_names

    def test_extract_nutrients(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("Add nitrogen, phosphorus, and potassium")
        nutrient_names = [e.name for e in entities if e.entity_type == "nutrient"]
        assert "nitrogen" in nutrient_names
        assert "phosphorus" in nutrient_names

    def test_extract_climate(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("Monitor temperature, humidity, and rainfall")
        climate_names = [e.name for e in entities if e.entity_type == "climate"]
        assert "temperature" in climate_names
        assert "humidity" in climate_names


# ─── Research Plugin Tests ─────────────────────────────────────────────────────

class TestResearchPlugin:
    def test_extract_hypotheses(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("The hypothesis and theory were tested")
        hyp_names = [e.name for e in entities if e.entity_type == "hypothesis"]
        assert "hypothesis" in hyp_names
        assert "theory" in hyp_names

    def test_extract_methods(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("Use experiment and survey methods")
        method_names = [e.name for e in entities if e.entity_type == "method"]
        assert "experiment" in method_names
        assert "survey" in method_names

    def test_extract_publications(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("Published in journal and conference")
        pub_names = [e.name for e in entities if e.entity_type == "publication"]
        assert "journal" in pub_names
        assert "conference" in pub_names

    def test_extract_metrics(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("Measure accuracy, precision, and recall")
        metric_names = [e.name for e in entities if e.entity_type == "metric"]
        assert "accuracy" in metric_names
        assert "precision" in metric_names


# ─── Benchmark Suite Tests ─────────────────────────────────────────────────────

class TestBenchmarkSuite:
    def test_add_and_get_results(self):
        suite = BenchmarkSuite()
        result = BenchmarkResult(id="1", vertical="healthcare", test_name="test1", passed=True, score=0.9, duration=0.1)
        suite.add_result(result)
        assert len(suite.get_results()) == 1

    def test_get_by_vertical(self):
        suite = BenchmarkSuite()
        suite.add_result(BenchmarkResult(id="1", vertical="healthcare", test_name="t1", passed=True, score=0.9, duration=0.1))
        suite.add_result(BenchmarkResult(id="2", vertical="legal", test_name="t2", passed=False, score=0.5, duration=0.2))
        assert len(suite.get_results(vertical="healthcare")) == 1

    def test_summary(self):
        suite = BenchmarkSuite()
        suite.add_result(BenchmarkResult(id="1", vertical="healthcare", test_name="t1", passed=True, score=0.9, duration=0.1))
        suite.add_result(BenchmarkResult(id="2", vertical="healthcare", test_name="t2", passed=False, score=0.5, duration=0.2))
        summary = suite.summary()
        assert summary["total"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1
