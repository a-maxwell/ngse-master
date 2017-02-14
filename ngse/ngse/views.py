""" Cornice services.
"""
from cornice import Service

v1_base = '/api/v1'


hello = Service(name='hello', path=v1_base, description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}

