from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateContactDTO:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    type: str
    siret: str

@dataclass
class UpdateContactDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    type: Optional[str] = None
    siret: Optional[str] = None


