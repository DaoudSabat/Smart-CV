# 📄 SmartCV

GPT-4 powered app that generates a professional one-page CV as a PDF from plain-text input.

## Overview

SmartCV takes raw career information from the user (skills, experience, projects, education) and uses GPT-4 to structure it into polished, A4-ready CV content. The result is rendered through Jinja2 HTML templates and exported as a PDF using pdfkit. Three template styles are available — default, modern, and classic.

## Architecture

```
smartcv/
├── core/
│   ├── cv_generator.py       # CVGenerator — GPT-4 content generation
│   └── template_renderer.py  # TemplateRenderer — Jinja2 → PDF via pdfkit
├── utils/
│   └── formatters.py         # to_bullets() — list → HTML <ul>
├── tests/
│   └── test_cv_generator.py  # pytest unit tests (OpenAI API mocked)
├── html_templates/
│   ├── default.html
│   ├── modern.html
│   └── classic.html
├── app.py                    # Streamlit entry point
└── .env.example
```

## Design Patterns

- **Facade** — `CVGenerator.generate()` hides all OpenAI prompt engineering and JSON parsing behind one method call
- **Strategy** — `TemplateRenderer` selects a rendering template at runtime (default / modern / classic) without changing the calling code
- **Factory Method** — `_detect_wkhtmltopdf()` auto-discovers the PDF binary across platforms (Linux, macOS, Windows)

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web UI and user input forms
- **OpenAI GPT-4** — structured CV content generation
- **Jinja2** — HTML template rendering
- **pdfkit + wkhtmltopdf** — HTML-to-PDF conversion
- **pytest** — unit testing

## Installation

```bash
git clone https://github.com/DaoudSabat/Smart-CV.git
cd Smart-CV
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

Install [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) for PDF export.

## Usage

```bash
streamlit run app.py
```

Fill in the form, select a template, and click **Generate CV** to download a ready-to-send PDF.

## Tests

```bash
pytest tests/ -v
```

All tests mock the OpenAI API — no API key or network required.

## License

MIT
