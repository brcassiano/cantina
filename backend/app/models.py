from pydantic import BaseModel, Field, condecimal
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class VendaCreate(BaseModel):
    """Schema para criar nova venda"""
    data: date = Field(..., description="Data da venda (não pode ser futura)")
    item: str = Field(..., min_length=1, max_length=100, description="Nome do item vendido")
    preco: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(..., description="Preço em reais")

    class Config:
        json_schema_extra = {
            "example": {
                "data": "2026-01-31",
                "item": "Suco de Laranja",
                "preco": 5.50
            }
        }


class VendaUpdate(BaseModel):
    """Schema para atualizar venda existente"""
    item: Optional[str] = Field(None, min_length=1, max_length=100)
    preco: Optional[condecimal(max_digits=10, decimal_places=2, gt=0)] = None


class VendaResponse(BaseModel):
    """Schema de resposta com dados da venda"""
    id: UUID
    data: date
    item: str
    preco: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TotalDiarioResponse(BaseModel):
    """Schema para total de vendas de um dia"""
    data: date
    total_faturado: float
    quantidade_itens: int


class TotalMensalResponse(BaseModel):
    """Schema para total de vendas de um mês"""
    mes: str
    total_faturado: float
    quantidade_itens: int