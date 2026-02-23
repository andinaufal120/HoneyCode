from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter(
    prefix="/modules",
    tags=["modules"]
)


class Settings(str, Enum):
    AVAIL_AT = "available_at"
    STOP_AT = "stop_at"


class Module(BaseModel):
    uuid: Optional[UUID] = None
    name: str
    module_num: int
    description: str = None
    settings: Optional[dict[Settings, str]] = None


fake_data: list[Module] = [
    Module(name="Variabel", module_num=2),
    Module(name="Operator", module_num=3),
    Module(name="Kondisi", module_num=4)
]


@router.get("/")
def get_modules():
    return fake_data


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_module(module: Module):
    fake_data.append(
        Module(uuid=uuid4(), name=module.name, module_num=module.module_num, description=module.description,
               settings=module.settings))


@router.get("/{uuid}")
def get_module(uuid: UUID):
    module: Module | None = next((module for module in fake_data if module.uuid == uuid), None)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return module


@router.put("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def update_module(uuid: UUID, new_data: Module):
    i, module = next(((i, module) for i, module in enumerate(fake_data) if module.uuid == uuid), None)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    updated = Module(uuid=module.uuid, name=new_data.name, module_num=new_data.module_num,
                     description=new_data.description, settings=new_data.settings)
    fake_data[i] = updated
