"""Configuration settings for the website."""

import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    
    # Site configuration
    SITE_TITLE = 'Anuroop Sriram'
    SITE_DESCRIPTION = 'Anuroop Sriram — leading AI for Science researcher (65 publications, h-index 40). Founding AI Research Scientist at Project Prometheus. Expert in model scaling (invented Graph Parallel training for GNNs), diffusion/flow matching for science, and post-training LLMs. Previously led AI for Science, fastMRI, and speech research at Meta FAIR. Created Open Catalyst, Open DAC, and OMC25 datasets. Built Deep Speech 2 at Baidu. First to scale speech models to billions of parameters.'
    SITE_BASEURL = ''
    SITE_URL = 'https://anuroopsriram.com'
    GOOGLE_ANALYTICS = 'G-H1K2L7JV60'
    GROUP_PUB_BY_YEAR = True
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    @classmethod
    def get_site_config(cls) -> Dict[str, Any]:
        """Get site configuration as dictionary."""
        return {
            'title': cls.SITE_TITLE,
            'name': cls.SITE_TITLE,
            'description': cls.SITE_DESCRIPTION,
            'baseurl': cls.SITE_BASEURL,
            'url': cls.SITE_URL,
            'google_analytics': cls.GOOGLE_ANALYTICS,
            'group_pub_by_year': cls.GROUP_PUB_BY_YEAR,
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SERVER_NAME = 'localhost'
    PREFERRED_URL_SCHEME = 'http'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}