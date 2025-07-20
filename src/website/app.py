"""Flask application factory for the academic website."""

from flask import Flask
from .config import config
from .data_loader import DataLoader
from .filters import register_filters
from .routes import main


def create_app(config_name: str = 'default') -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize data loader
    data_loader = DataLoader()
    
    # Register template context processor
    @app.context_processor
    def inject_site_data():
        """Inject site configuration and data into all templates."""
        site_config = config[config_name].get_site_config()
        site_config['data'] = data_loader.get_all_data()
        return {'site': site_config}
    
    # Register template filters
    register_filters(app)
    
    # Register blueprints
    app.register_blueprint(main)
    
    return app