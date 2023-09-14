from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfilePopulateDTO:
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
    country: str
    description: str
    date_of_birth: datetime
