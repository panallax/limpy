from pydantic import BaseModel

class InventoryCreate(BaseModel):
    name: str
    code: str
    manufacturer: str
    manufacturer_code: str
    current_stock: int
    min_stock: int
    location: str


