from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from services.label_printer import create_and_print_label

router = APIRouter()

class LabelData(BaseModel):
    product_name: str
    event_name: str
    barcode_data: str
    product_date: str
    storage_name: str
    storage_shelf: str
    storage_level: str
    note: str
    handler: str
    amount: Optional[int] = None
    unit: Optional[str] = None
    label_amount: int = 1

@router.post("/print")
async def print_label(label_data: LabelData):
    create_and_print_label(
        product_name=label_data.product_name,
        event_name=label_data.event_name,
        barcode_data=label_data.barcode_data,
        product_date=label_data.product_date,
        storage_name=label_data.storage_name,
        storage_shelf=label_data.storage_shelf,
        storage_level=label_data.storage_level,
        note=label_data.note,
        handler=label_data.handler,
        amount=label_data.amount,
        unit=label_data.unit,
        label_amount=label_data.label_amount
    )
    return {"message": "Druckauftrag wurde eingereicht."}
