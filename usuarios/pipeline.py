from requests import request, HTTPError

from django.core.files.base import ContentFile

from usuarios.models import Perfil

def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        changed = False  # flag to track changes
        protected = ('username', 'id', 'pk', 'email') + \
            tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
        for name, value in details.items():
            #print (name, value)
            if value and hasattr(user, name):
                # Check https://github.com/omab/python-social-auth/issues/671
                current_value = getattr(user, name, None)
                if not current_value or name not in protected:
                    changed |= current_value != value
                    setattr(user, name, value)

        if changed:
            strategy.storage.user.changed(user)

        # extra data #

        if not hasattr(user, 'perfil') or not user.perfil:
            perfil = Perfil(usuario=user)
        else:
            perfil = user.perfil

        gender = response.get('gender', '')

        if len(gender) > 0:
            sexo = gender[0].lower()

            if sexo in ['m', 'f']:
                perfil.sexo = sexo

        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            r = request('GET', url, params={'type': 'large'})
            r.raise_for_status()
        except HTTPError:
            pass
        else:
            perfil.imagen.save('{0}_social.jpg'.format(user.username), ContentFile(r.content))

        perfil.save()