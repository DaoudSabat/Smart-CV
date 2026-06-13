"""Unit tests for SmartCV — mocks the OpenAI API call."""
import json
from unittest.mock import MagicMock, patch

import pytest

from core.cv_generator import CVGenerator
from utils.formatters import to_bullets


# ---------- Formatter tests ----------

def test_to_bullets_list():
    result = to_bullets(["Python", "Django"])
    assert result == "<ul><li>Python</li><li>Django</li></ul>"


def test_to_bullets_empty_list():
    assert to_bullets([]) == "<ul></ul>"


def test_to_bullets_passthrough_string():
    assert to_bullets("already a string") == "already a string"


# ---------- CVGenerator tests ----------

_MOCK_RESPONSE = {
    "summary": "Experienced engineer.",
    "skills": ["Python", "SQL"],
    "education": "BSc Computer Science",
    "experience": ["Software engineer at XYZ"],
    "projects": ["Built REST API"],
    "languages": ["English - Native"],
}

def _make_mock_client():
    choice = MagicMock()
    choice.message.content = json.dumps(_MOCK_RESPONSE)
    completion = MagicMock()
    completion.choices = [choice]
    client = MagicMock()
    client.chat.completions.create.return_value = completion
    return client


def test_generate_returns_required_keys():
    gen = CVGenerator(api_key="test")
    gen._client = _make_mock_client()
    result = gen.generate({
        "name": "Daoud", "email": "d@test.com", "job_title": "Engineer",
        "skills": "Python", "experience": "3 years", "projects": "API",
        "education": "BSc", "languages": ["English - Native"],
    })
    for key in ("name", "email", "job_title", "summary", "skills", "education"):
        assert key in result


def test_generate_formats_skills_as_html():
    gen = CVGenerator(api_key="test")
    gen._client = _make_mock_client()
    result = gen.generate({
        "name": "Daoud", "email": "d@test.com", "job_title": "Engineer",
        "skills": "Python", "experience": "3 years", "projects": "API",
        "education": "BSc", "languages": [],
    })
    assert "<ul>" in result["skills"]


def test_generate_preserves_name():
    gen = CVGenerator(api_key="test")
    gen._client = _make_mock_client()
    result = gen.generate({
        "name": "Daoud Sabat", "email": "d@test.com", "job_title": "Engineer",
        "skills": "Python", "experience": "3 years", "projects": "API",
        "education": "BSc", "languages": [],
    })
    assert result["name"] == "Daoud Sabat"
