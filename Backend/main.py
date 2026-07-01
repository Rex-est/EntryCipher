from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from shared.database.connection import engine, Base
from shared.security.rate_limit import limiter

from app.auth.domain.entities import User
from app.events.domain.entities import Event, EventZone, PricingTier
from app.tickets.domain.entities import Ticket


origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:5173",
    "https://entrycipher-front-prod.onrender.com",
    "https://entrycipher-frontend.onrender.com",
]


app = FastAPI(
    title="SafeTicket Enterprise API",
    description="API Gateway y Core Services para la plataforma SafeTicket",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "OK",
        "message": "El motor de SafeTicket está en línea."
    }


from app.auth.presentation.routes import router as auth_router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])

from app.events.presentation.routes import router as events_router
app.include_router(events_router, prefix="/api/v1/events", tags=["Eventos"])

from app.tickets.presentation.routes import router as tickets_router
app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["Tickets"])

from app.admin.presentation.routes import router as admin_router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Administración"])