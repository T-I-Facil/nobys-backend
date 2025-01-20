from .security import registration, authentication
from .hospital import hospital
from .schedule import schedule

__all__ = [
    registration,
    authentication,
    hospital,
    schedule
]

routes = [route.router for route in __all__]