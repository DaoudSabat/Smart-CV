"""Jinja2 HTML template renderer with PDF output via pdfkit."""
from __future__ import annotations

import os
import shutil

import pdfkit
from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    """Renders a CV template to PDF given a sections dict."""

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "html_templates")
    WKHTMLTOPDF_PATHS = [
        "/usr/bin/wkhtmltopdf",
        "/usr/local/bin/wkhtmltopdf",
        "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe",
    ]
    PDF_OPTIONS = {
        "print-media-type": "",
        "page-size": "A4",
        "encoding": "UTF-8",
    }

    def __init__(self, template_name: str = "default") -> None:
        self.template_name = template_name
        self._config = self._detect_wkhtmltopdf()

    def _detect_wkhtmltopdf(self) -> pdfkit.configuration | None:
        """Auto-detect wkhtmltopdf binary; fall back to PATH."""
        for path in self.WKHTMLTOPDF_PATHS:
            if os.path.isfile(path):
                return pdfkit.configuration(wkhtmltopdf=path)
        found = shutil.which("wkhtmltopdf")
        if found:
            return pdfkit.configuration(wkhtmltopdf=found)
        return None

    def render_cv(self, sections: dict, output_file: str = "SmartCV.pdf") -> str:
        """Render sections into a PDF file and return the file path."""
        env = Environment(loader=FileSystemLoader(os.path.abspath(self.TEMPLATES_DIR)))
        template = env.get_template(f"{self.template_name}.html")
        html_content = template.render(sections)

        tmp_html = os.path.join(os.getcwd(), "_smartcv_tmp.html")
        with open(tmp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        try:
            kwargs = {"options": self.PDF_OPTIONS}
            if self._config:
                kwargs["configuration"] = self._config
            pdfkit.from_file(tmp_html, output_file, **kwargs)
        finally:
            if os.path.exists(tmp_html):
                os.remove(tmp_html)

        return output_file
