"""GPT-powered CV content generator."""
from __future__ import annotations

import json
import os

from openai import OpenAI

from utils.formatters import to_bullets


class CVGenerator:
    """Calls GPT-4 to produce structured CV content from raw user input."""

    MODEL = "gpt-4"
    SYSTEM_PROMPT = (
        "You are a professional CV writing assistant. "
        "Return only valid JSON — no markdown, no explanation."
    )

    def __init__(self, api_key: str | None = None) -> None:
        self._client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def generate(self, user_data: dict) -> dict:
        """Generate structured CV sections from user input dict.

        Args:
            user_data: keys — name, email, phone, address, linkedin,
                       job_title, skills, experience, projects,
                       education, languages (list[str])

        Returns:
            Flat dict of CV sections ready for template rendering.
        """
        prompt = self._build_prompt(user_data)
        response = self._client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        raw = response.choices[0].message.content.strip()
        generated = json.loads(raw)

        return {
            "name": user_data["name"],
            "email": user_data["email"],
            "phone": user_data.get("phone", ""),
            "address": user_data.get("address", ""),
            "linkedin": user_data.get("linkedin", ""),
            "job_title": user_data["job_title"],
            "summary": generated.get("summary", ""),
            "skills": to_bullets(generated.get("skills", [])),
            "education": generated.get("education", ""),
            "experience": to_bullets(generated.get("experience", [])),
            "projects": to_bullets(generated.get("projects", [])),
            "languages": to_bullets(generated.get("languages", user_data.get("languages", []))),
        }

    def _build_prompt(self, data: dict) -> str:
        languages_text = "\n".join(data.get("languages", []))
        return f"""
Generate a JSON object with this exact structure:
{{
  "summary": "...",
  "skills": ["...", "..."],
  "education": "...",
  "experience": ["...", "..."],
  "projects": ["...", "..."],
  "languages": ["..."]
}}
Tone: professional, concise, A4-page ready. Max 4-6 items per list.

Candidate:
Name: {data['name']}
Email: {data['email']}
Phone: {data.get('phone', '')}
Address: {data.get('address', '')}
LinkedIn: {data.get('linkedin', '')}
Job Title: {data['job_title']}
Skills: {data.get('skills', '')}
Experience: {data.get('experience', '')}
Projects: {data.get('projects', '')}
Education: {data.get('education', '')}
Languages: {languages_text}
"""
