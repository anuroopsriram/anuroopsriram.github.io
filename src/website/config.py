"""Configuration settings for the website."""

from __future__ import annotations

import os
from typing import Any


class Config:
    """Base configuration class."""

    # Site configuration
    SITE_TITLE = "Anuroop Sriram"
    SITE_DESCRIPTION = (
        "Anuroop Sriram builds foundation models, generative models, and automated "
        "research systems. Founding AI Research Scientist at Prometheus, building "
        "the Artificial General Engineer; previously led research teams at Meta FAIR "
        "across materials, medical imaging, and speech."
    )
    SITE_BASEURL = ""
    SITE_URL = "https://anuroopsriram.com"
    GOOGLE_ANALYTICS = "G-H1K2L7JV60"
    GROUP_PUB_BY_YEAR = True

    # Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    @classmethod
    def get_site_config(cls) -> dict[str, Any]:
        """Get site configuration as dictionary."""
        return {
            "title": cls.SITE_TITLE,
            "name": cls.SITE_TITLE,
            "description": cls.SITE_DESCRIPTION,
            "baseurl": cls.SITE_BASEURL,
            "url": cls.SITE_URL,
            "google_analytics": cls.GOOGLE_ANALYTICS,
            "group_pub_by_year": cls.GROUP_PUB_BY_YEAR,
        }


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SERVER_NAME = "localhost"
    PREFERRED_URL_SCHEME = "http"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
