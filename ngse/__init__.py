"""Main entry point
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.include("pyramid_mailer")
    config.include("pyramid_jinja2")
    config.add_jinja2_renderer('.html')
    # # config.add_static_view('assets', 'static/assets', cache_max_age=3600)
    config.add_static_view('static', 'static')
    config.add_route('index', '/')
    config.add_static_view('templates', 'templates')
    config.scan("ngse.views")
    return config.make_wsgi_app()
