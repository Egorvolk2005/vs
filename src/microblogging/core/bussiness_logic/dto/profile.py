from dataclasses import dataclass 
from typing import Optional, Union
from datetime import datetime 
from django.core.files.uploadedfile import InMemoryUploadedFile 
 
@dataclass 
class ProfileDTO: 
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    email: Optional[str]
    country: Optional[str]
    photo: Optional[InMemoryUploadedFile]
    description: Optional[str]
    date_of_birth: Optional[str]
    date_joined: Optional[datetime]
