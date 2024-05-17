from pydantic import BaseModel

class Material(BaseModel):
    code: str
    object_name: str
    unit_of_measurement: str
