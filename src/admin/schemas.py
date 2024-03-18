from typing import List

from pydantic import BaseModel

class UserListRs(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role_id: int
    is_active: bool
class TemplateSearchRs(BaseModel):
    status: str
    data: List[UserListRs]
    details: str|None = None
