Building a TG2.1 app with ldap auth
===================================

Here are some commands (on Fedora 15) to get you setup with a fresh app::

    $ mkvirtualenv --no-site-packages repoze-ldap-app
    $ pip install tg.devtools
    $ paster quickstart   # call the pp repoze-ldap-app, yes to mako and auth
    $ cd repoze-ldap-app
    $ python setup.py develop
    $ pip install genshi  # This is a workaround.
    $ paster setup-app development.ini
    $ paster serve development.ini  # To test if the basic app works.


Add repoze.who.plugins.ldap to setup.py && python setup.py develop

Add ``who.ini`` file.

Reference ``who.ini`` file in ``development.ini`` and ``production.ini``.

Edit ``repozeldapapp/config/middleware.py``

Add ``repozeldapapp/lib/auth.py``.
