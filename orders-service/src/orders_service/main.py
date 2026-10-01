from fastapi import FastAPI

from orders_service.infrastructure.api.routes import router as orders_router

app = FastAPI(
    title="Orders Service API",
    description="Microservicio para la gestión de pedidos (Arquitectura Hexagonal)",
    version="1.0.0",
)

app.include_router(orders_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
