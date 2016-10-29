from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

#__all__ = ['get_model_path', 'get_custom_model', 'is_abstract']

_COMPLETE_MODELS = {
    'TIGERLINE_ZIPCODE_MODEL': 'tigerline.Zipcode',
    'TIGERLINE_NATION_MODEL': 'tigerline.Nation',
    'TIGERLINE_DIVISION_MODEL': 'tigerline.Division',
    'TIGERLINE_STATE_MODEL': 'tigerline.StateComplete',
    'TIGERLINE_COUNTY_MODEL': 'tigerline.CountyComplete',
    'TIGERLINE_SUBCOUNTY_MODEL': 'tigerline.SubCountyComplete'
}

_DEFAULT_MODELS = {
    'TIGERLINE_STATE_MODEL': 'tigerline.StateComplete',
    'TIGERLINE_COUNTY_MODEL': 'tigerline.CountyComplete',
    'TIGERLINE_SUBCOUNTY_MODEL': 'tigerline.SubCountyComplete'
}

def _get_complete(setting):
    try:
        return _COMPLETE_MODELS[setting]
    except KeyError:
        raise ImproperlyConfigured(
            "%s - unknown setting name. See documentation for list of available models"
            " and their setting names." % setting)


def is_abstract(setting):
    return getattr(settings, setting, None) != _get_complete(setting)
        

def get_tigerline_model_name(setting):
    """
    Returns the model name for a particular setting name.
    """
    # make sure the setting name is correct
    complete_model_name = _get_complete(setting)
    model_name = getattr(settings, setting, None)
    if model_name is None:
        if getattr(settings, 'TIGERLINE_COMPLETE_SETUP', False):
            return complete_model_name
        try:
            model_name = _DEFAULT_MODELS[setting]
        except KeyError:
            raise ImproperlyConfigured(
                "%s was requested, is not configured in settings." % setting)
    return model_name


def get_tigerline_model(setting):
    """
    Returns the model for a particular setting name.
    """
    model_name = get_tigerline_model_name(setting)
    try:
        return apps.get_model(model_name)
    except ValueError:
        raise ImproperlyConfigured(
            "%s must be of the form 'app_label.model_name'" % setting)
    except LookupError:
        raise ImproperlyConfigured(
            "%s refers to model '%s' that has not been installed" % (setting, model_name))
