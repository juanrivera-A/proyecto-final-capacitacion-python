from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from orders_service.application.dtos import CreateOrderInputDTO, OrderItemDTO
from orders_service.application.use_cases import OrderUseCases
from orders_service.domain.exceptions import DomainError
from orders_service.infrastructure.api.dependencies import get_use_cases
from orders_service.infrastructure.api.schemas import CreateOrderRequest, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

# Definición con Annotated para evitar B008
UseCasesDep = Annotated[OrderUseCases, Depends(get_use_cases)]


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: CreateOrderRequest,
    use_cases: UseCasesDep,
) -> OrderResponse:
    try:
        input_dto = CreateOrderInputDTO(
            customer_id=payload.customer_id,
            items=[
                OrderItemDTO(
                    product_id=item.product_id, quantity=item.quantity, price=item.price
                )
                for item in payload.items
            ],
        )
        result = use_cases.create_order(input_dto)

        return OrderResponse.model_validate(result)

    except DomainError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except Exception as err:
        # Esto te mostrará en la respuesta JSON cualquier otro error de serialización
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unhandled error: {type(err).__name__} - {err!s}",
        ) from err


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    use_cases: UseCasesDep,
) -> OrderResponse:
    order = use_cases.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id '{order_id}' not found.",
        )
    return order  # type: ignore[return-value]


@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(
    order_id: str,
    use_cases: UseCasesDep,
) -> OrderResponse:
    try:
        return use_cases.pay_order(order_id)  # type: ignore[return-value]
    except DomainError as err:
        if "not found" in str(err).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
            ) from err
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: str,
    use_cases: UseCasesDep,
) -> OrderResponse:
    try:
        return use_cases.cancel_order(order_id)  # type: ignore[return-value]
    except DomainError as err:
        if "not found" in str(err).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
            ) from err
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err


@router.get("", response_model=list[OrderResponse])
def list_orders(
    use_cases: UseCasesDep,
) -> list[OrderResponse]:
    return use_cases.list_orders()  # type: ignore[return-value]
