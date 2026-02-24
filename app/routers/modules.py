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


class ModuleBase(BaseModel):
    """
    Represents a base class for modules in the system.

    This class serves as a foundational structure for modules that may hold
    information such as the module's name, a module number, optional descriptive
    text, and module configuration settings. It provides a flexible interface
    for extending or creating module-based structures.

    :ivar name: The name of the module.
    :type name: str
    :ivar module_num: A unique numeric identifier for the module.
    :type module_num: int
    :ivar description: Optional descriptive text about the module's purpose
        or functionality.
    :type description: Optional[str]
    :ivar settings: Optional dictionary of settings with keys representing
        configuration options and their associated string values.
    :type settings: Optional[dict[Settings, str]]
    """
    name: str
    module_num: int
    description: Optional[str] = None
    settings: Optional[dict[Settings, str]] = None


class ModuleOut(ModuleBase):
    """
    Represents an output module in the system.

    This class extends the ModuleBase parent class designed to define
    the behavior and properties of an output module. It contains an
    identifier for the module, which is a universally unique identifier
    (UUID).

    :ivar uuid: Universally unique identifier for the module instance.
    :type uuid: UUID
    """
    uuid: UUID


class ModuleInDB(ModuleBase):
    """
    Represents a Module entity stored in the database.

    This class extends the ModuleBase class and adds additional
    attributes specifically needed for database representation.
    It contains identifiers for the module, including both
    numerical and universally unique identifiers.

    :ivar id: The numerical identifier for the module in the database.
    :type id: int
    :ivar uuid: Universally unique identifier for the module instance.
    :type uuid: UUID
    """
    id: int
    uuid: UUID



fake_data: list[ModuleOut] = [
    ModuleOut(name="Variabel", module_num=2, uuid=uuid4()),
    ModuleOut(name="Operator", module_num=3, uuid=uuid4()),
    ModuleOut(name="Kondisi", module_num=4, uuid=uuid4())
]


@router.get("/", status_code=status.HTTP_200_OK)
def get_modules() -> list[ModuleOut]:
    """
    Return all modules.
    :return: List of modules
    """
    if not fake_data:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No modules yet")
    return fake_data


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_module(module: ModuleBase) -> None:
    fake_data.append(
        ModuleOut(uuid=uuid4(), name=module.name, module_num=module.module_num, description=module.description,
               settings=module.settings))


@router.get("/{uuid}")
def get_module(uuid: UUID):
    module: ModuleOut | None = next((module for module in fake_data if module.uuid == uuid), None)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return module


@router.put("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def update_module(uuid: UUID, new_data: ModuleOut):
    i, module = next(((i, module) for i, module in enumerate(fake_data) if module.uuid == uuid), None)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    updated = ModuleOut(uuid=module.uuid, name=new_data.name, module_num=new_data.module_num,
                     description=new_data.description, settings=new_data.settings)
    fake_data[i] = updated
