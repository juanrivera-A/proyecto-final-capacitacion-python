from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemRequest(BaseModel):
    product_id: str = Field(..., min_length=1, description="ID único del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto (mayor a 0)")
    price: Decimal = Field(..., gt=0, description="Precio unitario (mayor a 0)")


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=1, description="ID del cliente")
    items: list[OrderItemRequest] = Field(
        ..., min_length=1, description="Lista de productos"
    )


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    quantity: int
    price: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_id: str
    status: str
    total_amount: Decimal
    items: list[OrderItemResponse]
