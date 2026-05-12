from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.database.connection import engine, Base

from app.auth.domain.entities import User 
# 👇 1. Importamos la entidad Event para que se cree la tabla
from app.events.domain.entities import Event # ... arriba con las demás importaciones
from app.tickets.domain.entities import Ticket

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:5173",
]

app = FastAPI(
    title="SafeTicket Enterprise API",
    description="API Gateway y Core Services para la plataforma SafeTicket",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 👈 Prueba con "*" solo para descartar que sea el origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "OK", "message": "El motor de SafeTicket está en línea."}

from app.auth.presentation.routes import router as auth_router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])

# 👇 2. Importamos y registramos las rutas de eventos
from app.events.presentation.routes import router as events_router
app.include_router(events_router, prefix="/api/v1/events", tags=["Eventos"])

from app.tickets.presentation.routes import router as tickets_router
app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["Tickets"])