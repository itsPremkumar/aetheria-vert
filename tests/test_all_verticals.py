"""Comprehensive tests for all vertical plugins."""
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

    def test_extract_obligations(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("The payment and delivery obligations")
        obligation_names = [e.name for e in entities if e.entity_type == "obligation"]
        assert "payment" in obligation_names

    def test_extract_relations(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("plaintiff has payment obligation")
        relations = plugin.extract_relations(entities, "plaintiff has payment obligation")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = LegalPlugin()
        entities = plugin.extract_entities("plaintiff defendant contract")
        result = plugin.reason(entities, "query")
        assert "plaintiff" in result.lower() or "defendant" in result.lower()


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

    def test_extract_financial_statements(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("Review the balance sheet and income statement")
        statement_names = [e.name for e in entities if e.entity_type == "financial_statement"]
        assert "balance sheet" in statement_names

    def test_extract_relations(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("stock subject to SEC regulation")
        relations = plugin.extract_relations(entities, "stock subject to SEC regulation")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = FinancePlugin()
        entities = plugin.extract_entities("stock bond SEC market risk")
        result = plugin.reason(entities, "query")
        assert "stock" in result.lower() or "bond" in result.lower()


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

    def test_extract_credentials(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("Earn a degree, diploma, or certificate")
        credential_names = [e.name for e in entities if e.entity_type == "credential"]
        assert "degree" in credential_names

    def test_extract_relations(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("mathematics requires critical thinking")
        relations = plugin.extract_relations(entities, "mathematics requires critical thinking")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = EducationPlugin()
        entities = plugin.extract_entities("mathematics science critical thinking")
        result = plugin.reason(entities, "query")
        assert "mathematics" in result.lower() or "science" in result.lower()


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

    def test_extract_sentiments(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("The customer was satisfied and happy")
        sentiment_names = [e.name for e in entities if e.entity_type == "sentiment"]
        assert "satisfied" in sentiment_names

    def test_extract_agents(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("The support agent and supervisor helped")
        agent_names = [e.name for e in entities if e.entity_type == "agent"]
        assert "support agent" in agent_names

    def test_extract_relations(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("complaint handled via email")
        relations = plugin.extract_relations(entities, "complaint handled via email")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = CustomerServicePlugin()
        entities = plugin.extract_entities("complaint email resolved")
        result = plugin.reason(entities, "query")
        assert "complaint" in result.lower() or "email" in result.lower()


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

    def test_extract_supply_chain(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("The supplier and warehouse managed inventory")
        supply_names = [e.name for e in entities if e.entity_type == "supply_chain"]
        assert "supplier" in supply_names

    def test_extract_safety(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("Use PPE and conduct hazard assessment")
        safety_names = [e.name for e in entities if e.entity_type == "safety"]
        assert "ppe" in safety_names

    def test_extract_relations(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("assembly uses CNC")
        relations = plugin.extract_relations(entities, "assembly uses CNC")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = ManufacturingPlugin()
        entities = plugin.extract_entities("assembly CNC ISO 9001")
        result = plugin.reason(entities, "query")
        assert "assembly" in result.lower() or "cnc" in result.lower()


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

    def test_extract_relations(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("wheat grows in clay")
        relations = plugin.extract_relations(entities, "wheat grows in clay")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = AgriculturePlugin()
        entities = plugin.extract_entities("wheat clay nitrogen temperature")
        result = plugin.reason(entities, "query")
        assert "wheat" in result.lower() or "clay" in result.lower()


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

    def test_extract_domains(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("Research in AI and machine learning")
        domain_names = [e.name for e in entities if e.entity_type == "domain"]
        assert "ai" in domain_names or "machine learning" in domain_names

    def test_extract_relations(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("experiment tests hypothesis")
        relations = plugin.extract_relations(entities, "experiment tests hypothesis")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = ResearchPlugin()
        entities = plugin.extract_entities("hypothesis experiment journal")
        result = plugin.reason(entities, "query")
        assert "hypothesis" in result.lower() or "experiment" in result.lower()
