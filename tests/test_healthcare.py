"""Tests for Healthcare Vertical Plugin."""
from __future__ import annotations

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from aetheria.verticals.healthcare import HealthcarePlugin


class TestHealthcarePlugin:
    def test_create_plugin(self):
        plugin = HealthcarePlugin()
        assert plugin.name == "healthcare"

    def test_extract_diseases(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient has diabetes and hypertension")
        disease_names = [e.name for e in entities if e.entity_type == "disease"]
        assert "diabetes" in disease_names
        assert "hypertension" in disease_names

    def test_extract_symptoms(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient reports fever, cough, and fatigue")
        symptom_names = [e.name for e in entities if e.entity_type == "symptom"]
        assert "fever" in symptom_names
        assert "cough" in symptom_names

    def test_extract_drugs(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient takes metformin and insulin")
        drug_names = [e.name for e in entities if e.entity_type == "drug"]
        assert "metformin" in drug_names
        assert "insulin" in drug_names

    def test_extract_treatments(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient underwent chemotherapy and surgery")
        treatment_names = [e.name for e in entities if e.entity_type == "treatment"]
        assert "chemotherapy" in treatment_names
        assert "surgery" in treatment_names

    def test_extract_procedures(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient had MRI and blood test")
        procedure_names = [e.name for e in entities if e.entity_type == "procedure"]
        assert "mri" in procedure_names
        assert "blood test" in procedure_names

    def test_extract_anatomy(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient has heart and lung condition")
        anatomy_names = [e.name for e in entities if e.entity_type == "anatomy"]
        assert "heart" in anatomy_names
        assert "lung" in anatomy_names

    def test_extract_relations(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("metformin treats diabetes")
        relations = plugin.extract_relations(entities, "metformin treats diabetes")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = HealthcarePlugin()
        entities = plugin.extract_entities("Patient has diabetes and takes metformin")
        result = plugin.reason(entities, "What is the treatment?")
        assert "diabetes" in result.lower() or "metformin" in result.lower()
