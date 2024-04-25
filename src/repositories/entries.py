from datetime import date as dateType
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ActionEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    date: dateType = Field(..., prompt='Enter action date')
    name: str | bool = Field(..., prompt='Enter action name')
    every_year: bool = Field(..., prompt='Action happens every year?')

    @field_validator('every_year', mode='before')
    def coerse_year_to_bool(cls, v):
        if isinstance(v, bool):
            return v
        elif isinstance(v, str):
            v_lower = v.lower()
            if v_lower == 'yes':
                return True
            elif v_lower == 'no':
                return False
        raise ValueError("my_attribute must be 'yes', 'no', True, or False")


class ActivityCodeEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    name: str
    date: dateType


class ContactEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = None
    fullname: str = Field(..., prompt='Enter contact name')
    birthdate: dateType = Field(..., prompt='Enter contact birth date')
    phone: str = Field(..., prompt='Enter contact phone')
    level: str = Field(..., prompt='Enter contact level')
    city: str = Field(..., prompt='Enter contact city')
    additional_info: str = Field(..., prompt='Enter contact additional info')
    profession: str = Field(..., prompt='Enter contact profession')

    #TODO validation here