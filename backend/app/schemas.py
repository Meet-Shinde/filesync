from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

class DeviceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_name = value.strip()

        if not cleaned_name:
            raise ValueError("Device name cannot be empty.")
        
        return cleaned_name

class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    created_at: datetime
    last_seen_at: datetime