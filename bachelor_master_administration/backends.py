from djangosaml2.backends import Saml2Backend
import logging
from typing import Any, Optional, Tuple
from django.conf import settings
from django.core.exceptions import (ImproperlyConfigured,
                                    MultipleObjectsReturned)

logger = logging.getLogger('djangosaml2')

class CustomSaml2Backend(Saml2Backend):
    def is_authorized(self, attributes, attribute_mapping):
        if attributes.get('hrEduPersonHomeOrg', [''])[0]=='riteh.hr':
            return True
        return False

    def get_or_create_user(self,
            user_lookup_key: str, user_lookup_value: Any, create_unknown_user: bool,
            idp_entityid: str, attributes: dict, attribute_mapping: dict, request
        ) -> Tuple[Optional[settings.AUTH_USER_MODEL], bool]:
        """ Look up the user to authenticate. If he doesn't exist, this method creates him (if so desired).
            The default implementation looks only at the user_identifier. Override this method in order to do more complex behaviour,
            e.g. customize this per IdP.
        """
        UserModel = self._user_model

        # Construct query parameters to query the userModel with. An additional lookup modifier could be specified in the settings.
        user_query_args = {
            user_lookup_key + getattr(settings, 'SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP', ''): user_lookup_value
        }

        # Lookup existing user
        # Lookup existing user
        user, created = None, False
        try:
            user = UserModel.objects.get(**user_query_args)
        except MultipleObjectsReturned:
            logger.error("Multiple users match, model: %s, lookup: %s", UserModel._meta, user_query_args)
        except UserModel.DoesNotExist:
            # Create new one if desired by settings
            if create_unknown_user:
                user = UserModel(**{ user_lookup_key: user_lookup_value })
                user.save()
                if attributes.get('hrEduPersonPrimaryAffiliation', [''])[0]=='student':
                	user.roles.add(1)
                else:
                	user.roles.add(2)
                created = True
                logger.debug('New user created: %s', user)
            else:
                logger.error('The user does not exist, model: %s, lookup: %s', UserModel._meta, user_query_args)

        return user, created
    