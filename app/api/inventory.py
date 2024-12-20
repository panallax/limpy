from fastapi import APIRouter, HTTPException
from app.models.inventory import InventoryCreate
from app.db.mongo import mongo_manager

inventory_router = APIRouter()
inventory_collection = mongo_manager.get_collection("inventory")

@inventory_router.post("/inventory")
def add_item(item: InventoryCreate):
    if inventory_collection.find_one({"name": item.name}):
        raise HTTPException(status_code=409, detail="El item ya existe")

    new_item = {
        "name": item.name,
        "code": item.code,
        "manufacturer": item.manufacturer,
        "manufacturer_code": item.manufacturer_code,
        "current_stock": item.current_stock,
        "min_stock": item.min_stock,
        "location": item.location

    }

    result = inventory_collection.insert_one(new_item)

    return {"message": "Item creado exitosamente", "id": str(result.inserted_id)}

@inventory_router.get("/inventory")
def get_inventory():
    inventory = inventory_collection.find()
    inventory_list = [
        {
            "id": str(item["_id"]),
            "name": item["name"],
            "code": item["code"],
            "manufacturer": item["manufacturer"],
            "manufacturer_code": item["manufacturer_code"],
            "current_stock": item["current_stock"],
            "min_stock": item["min_stock"],
            "location": item["location"]
        }
        for item in inventory
    ]
    return inventory_list

@inventory_router.delete("/inventory/{item_id}")

def delete_item(item_id: str):
    result = inventory_collection.delete_one({"_id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": f"Item {item_id} deleted successfully"}

@inventory_router.put("/inventory/{item_id}")
def update_item(item_id: str, item: InventoryCreate):
    result = inventory_collection.update_one({"_id": item_id}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": f"Item {item_id} updated successfully"}

@inventory_router.get("/inventory/{item_id}")
def get_item(item_id: str):
    item = inventory_collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "code": item["code"],
        "manufacturer": item["manufacturer"],
        "manufacturer_code": item["manufacturer_code"],
        "current_stock": item["current_stock"],
        "min_stock": item["min_stock"],
        "location": item["location"]
    }

@inventory_router.get("/inventory/{item_id}/stock")
def get_stock(item_id: str):
    item = inventory_collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"current_stock": item["current_stock"], "min_stock": item["min_stock"]}
