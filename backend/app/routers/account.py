from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any

from ..services.account import get_all_positions, upsert_position, remove_position

router = APIRouter()

class PositionModel(BaseModel):
    code: str
    cost: float
    shares: float

@router.get("/account/positions")
def get_positions():
    try:
        return get_all_positions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/account/positions")
def update_position(data: PositionModel):
    try:
        upsert_position(data.code, data.cost, data.shares)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/account/positions/{code}")
def delete_position(code: str):
    try:
        remove_position(code)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
