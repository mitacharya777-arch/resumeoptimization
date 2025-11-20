"""
Resume Template System
Implements three professional resume templates:
1. Professional Modern - Blue accents, professional style
2. Tech Minimalist - Minimal, ATS-optimized
3. Data Professional - Teal accents, structured layout
"""

from typing import Dict


def get_template(template_name: str) -> Dict:
    """Get template configuration by name."""
    templates = {
        "professional_modern": {
            "name": "Professional Modern",
            "description": "Best for corporate positions, business roles, traditional companies",
            "accent_color": "#2563eb",
            "section_underline": True,
            "header_border": True,
            "style": "professional"
        },
        "tech_minimalist": {
            "name": "Tech Minimalist",
            "description": "Best for tech companies, startups, ATS-optimized",
            "accent_color": "#000000",
            "section_underline": False,
            "header_border": False,
            "style": "minimal"
        },
        "data_professional": {
            "name": "Data Professional",
            "description": "Best for data analyst/scientist roles, research positions",
            "accent_color": "#14b8a6",
            "section_underline": True,
            "header_border": True,
            "style": "structured"
        }
    }
    return templates.get(template_name.lower(), templates["professional_modern"])


def get_all_templates() -> Dict:
    """Get all available templates."""
    return {
        "professional_modern": get_template("professional_modern"),
        "tech_minimalist": get_template("tech_minimalist"),
        "data_professional": get_template("data_professional")
    }