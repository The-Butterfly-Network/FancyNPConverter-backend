from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class NPCLocation(BaseModel):
    world: str
    x: float
    y: float
    z: float
    yaw: float
    pitch: float

class NPCSkin(BaseModel):
    identifier: Optional[str] = None
    variant: str = "AUTO"  # AUTO, SLIM
    mirrorSkin: bool = False

class NPCAction(BaseModel):
    action: str
    value: str

class NPCEquipment(BaseModel):
    HEAD: Optional[Dict[str, Any]] = None
    CHEST: Optional[Dict[str, Any]] = None
    LEGS: Optional[Dict[str, Any]] = None
    FEET: Optional[Dict[str, Any]] = None
    HAND: Optional[Dict[str, Any]] = None
    OFF_HAND: Optional[Dict[str, Any]] = None

class FancyNPC(BaseModel):
    name: str
    creator: str
    displayName: str = "<empty>"
    type: str = "PLAYER"
    location: NPCLocation
    showInTab: bool = False
    spawnEntity: bool = True
    collidable: bool = True
    glowing: bool = False
    glowingColor: str = "white"
    turnToPlayer: bool = True
    turnToPlayerDistance: int = -1
    interactionCooldown: float = 0.0
    scale: float = 1.0
    visibility_distance: int = 80
    skin: NPCSkin
    actions: Optional[Dict[str, Dict[str, NPCAction]]] = None
    equipment: Optional[NPCEquipment] = None
    attributes: Optional[Dict[str, str]] = None

class ConversionResponse(BaseModel):
    message: str
    npcs_converted: int
    output_format: str

class ConverterInfo(BaseModel):
    name: str
    description: str
    supported_formats: Dict[str, str]
    features: List[str]