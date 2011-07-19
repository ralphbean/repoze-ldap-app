from repoze.who.plugins.ldap import (
    LDAPAttributesPlugin, LDAPAuthenticatorPlugin
)
import ldap


class URISaver(object):
    """ Saves the ldap_connection str given to repoze authn and authz """
    def __init__(self, *args, **kw):
        self.uri = kw['ldap_connection']
        super(URISaver, self).__init__(*args, **kw)


class ReconnectingLDAPAttrsPlugin(LDAPAttributesPlugin, URISaver):
    """ Gets attributes from LDAP.  Refreshes connection if stale. """

    def add_metadata(self, environ, identity):
        """ Add ldap attributes to the `identity` entry. """

        try:
            return super(ReconnectingLDAPAttrsPlugin, self).add_metadata(
                environ, identity)
        except Exception, e:
            print "FAILED TO CONNECT TO LDAP 1 : " + str(e)
            print "Retrying..."
            self.ldap_connection = ldap.initialize(self.uri)
            return super(ReconnectingLDAPAttrsPlugin, self).add_metadata(
                environ, identity)


class ReconnectingAuthenticatorPlugin(LDAPAuthenticatorPlugin, URISaver):
    """ Authenticates against LDAP.

    - Refreshes connection if stale.
    - Denies anonymously-authenticated users

    """

    def authenticate(self, environ, identity):
        """ Extending the repoze.who.plugins.ldap plugin to make it much
        more secure. """

        res = None

        try:
            # This is unbelievable.  Without this, ldap will
            #   let you bind anonymously
            if not identity.get('password', None):
                return None
            try:
                dn = self._get_dn(environ, identity)
            except (KeyError, TypeError, ValueError):
                return None

            res = super(ReconnectingAuthenticatorPlugin, self).authenticate(
                environ, identity)

            # Sanity check here (for the same reason as the above check)
            if "dn:%s" % dn != self.ldap_connection.whoami_s():
                return None

        except ldap.LDAPError, e:
            print "FAILED TO CONNECT TO LDAP 2 : " + str(e)
            print "Retrying..."
            self.ldap_connection = ldap.initialize(self.uri)

        return res
