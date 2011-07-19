# -*- coding: utf-8 -*-
"""WSGI middleware initialization for the repoze-ldap-app application."""

from repozeldapapp.config.app_cfg import base_config
from repozeldapapp.config.environment import load_environment

from repoze.who.config import make_middleware_with_config


__all__ = ['make_app']

# Use base_config to setup the necessary PasteDeploy application factory. 
# make_base_app will wrap the TG2 app with all the middleware it needs. 
make_base_app = base_config.setup_tg_wsgi_app(load_environment)


def make_app(global_conf, full_stack=True, **app_conf):
    """
    Set repoze-ldap-app up with the settings found in the PasteDeploy configuration
    file used.
    
    :param global_conf: The global settings for repoze-ldap-app (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The repoze-ldap-app application with all the relevant middleware
        loaded.
    
    This is the PasteDeploy factory for the repoze-ldap-app application.
    
    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.
    
   
    """
    app = make_base_app(global_conf, full_stack=True, **app_conf)
    
    # Wrap your base TurboGears 2 application with custom middleware here
    app = make_middleware_with_config(
        app, global_conf,
        app_conf['who.config_file'],
        app_conf['who.log_stream'],
        app_conf['who.log_level'])

    
    return app
