import six
import sys

from django.conf import settings as s

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


class SuStateMiddleware(object):
    su_state_fqcn = getattr(s, "SU_STATE_CLASS", "django_switchuser.state.SuState")
    su_state_module_n, _, su_state_class_n = su_state_fqcn.rpartition(".")
    su_state_module = import_module(su_state_module_n)
    su_state_class = getattr(su_state_module, su_state_class_n)

    def process_request(self, request):
        try:
            request.su_state = self.su_state_class(request)
        except AttributeError as error:
            if not hasattr(request, "user"):
                raise self.get_su_config_error(
                    error,
                    str(error) + " (NOTE: django_switchuser must be **after** "
                    "django.contrib.auth.middleware.AuthenticationMiddleware!)"
                )
            raise

    def get_su_config_error(self, error, message):
        if six.PY2:
            return AttributeError(message), None, sys.exc_info()[2]
        else:
            return error.with_traceback(message)
