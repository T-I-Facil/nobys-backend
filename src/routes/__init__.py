from .v1.authentication import router as authentication_router
from .v1.registration import router as registration_router
from .v1.hospital import router as hospital_router
from .v1.schedule import router as schedule_router
from .v1.me import router as me_router
from .v1.invoices import router as invoices_router
from .v1.analytics import router as analytics_router

routes = [
    authentication_router,
    registration_router,
    hospital_router,
    schedule_router,
    me_router,
    invoices_router,
    analytics_router
]