from .security import registration, authentication

__all__ = [
    registration,
    authentication
]

routes = [route.router for route in __all__]