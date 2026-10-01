import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from orders_service.infrastructure.api.routes import router as orders_router

app = FastAPI(
    title="Orders Service API",
    description="Microservicio para la gestión de pedidos (Arquitectura Hexagonal)",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n" + "=" * 50)
    print("ERROR CAPTURADO EN TIEMPO DE EJECUCIÓN:")
    traceback.print_exc()
    print("=" * 50 + "\n")
    return JSONResponse(
        status_code=500, content={"detail": str(exc), "type": type(exc).__name__}
    )


app.include_router(orders_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
