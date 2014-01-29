from django.conf import settings
from django.db.models.loading import get_model

__all__ = ['get_model_path', 'get_custom_model', 'is_abstract']

DEFAULT_MODELS = (
    ('zipcode', 'tigerline1.Zipcode'),
    ('nation', 'tigerline1.Nation'),
    ('division', 'tigerline1.Division'),
    ('state', 'tigerline1.State'),
    ('county', 'tigerline1.County'),
    ('subcounty', 'tigerline1.SubCounty')
)

MODELS = getattr(settings, 'TIGERLINE_MODELS', ())


def get_model_path(obj_name):
    return dict(DEFAULT_MODELS + MODELS).get(obj_name)

def get_custom_model(obj_name):
    model_name = get_model_path(obj_name)
    if model_name is None:
        return None
    return get_model(*model_name.split('.'))

def is_abstract(obj_name):
    return get_model_path(obj_name) != dict(DEFAULT_MODELS).get(obj_name)