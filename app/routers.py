from pathlib import Path
from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from app.models import Item, PydanticObjectId
from app.services import ItemService, get_item_service

router = APIRouter()

@router.get("/")
async def root():
    return "Wer das liest ist doof!"

@router.post("/items/")
async def create_item(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    item: Item, 
    ) -> Item:
    new_item = await item_service.create(item)
    created_item = await item_service.get(new_item.id)
    if created_item is not None:
        return created_item
    raise HTTPException(status_code=500, detail="Item could not be created")

@router.get("/items/{itemId}")
async def get_item(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    item_id: Annotated[PydanticObjectId, Path(alias="itemId")],
) -> Item:
    item = await item_service.get(item_id)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{itemId}")
async def update_item(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    item_id: Annotated[PydanticObjectId, Path(alias="itemId")],
    payload: dict[str, Any],
) -> Item:
    updated_count = await item_service.update(item_id, payload)
    if updated_count > 0:
        updated_item = await item_service.get(item_id)
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{itemId}")
async def delete_item(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    item_id: Annotated[PydanticObjectId, Path(alias="itemId")],
) -> int:
    deleted_count = await item_service.delete(item_id)
    if deleted_count > 0:
        return deleted_count
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/items/")
async def list_items(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    item_ids: Annotated[list[PydanticObjectId], Query(alias="itemIds")] = None,
    ) -> list[Item]:
    items = await item_service.list(item_ids)
    return items