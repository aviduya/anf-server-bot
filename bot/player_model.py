from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class PlayerBase(BaseModel):
    uuid: str
    name: str
    avatar: HttpUrl
    render: HttpUrl

class OppedPlayer(PlayerBase):
    level: int
    bypassesPlayerLimit: bool

class BannedPlayer(PlayerBase):
    reason: str

class BannedIP(BaseModel):
    ip: str
    reason: str

class Banned(BaseModel):
    players: List[BannedPlayer]
    ips: List[BannedIP]

class Whitelist(BaseModel):
    enabled: bool
    list: List[PlayerBase]

class Players(BaseModel):
    online: int
    max: int
    list: List[PlayerBase]

class ServerPlayerModel(BaseModel):
    success: bool
    online: bool
    online_mode: bool
    opped: List[OppedPlayer]
    banned: Banned
    whitelist: Whitelist
    players: Optional[Players] = None
