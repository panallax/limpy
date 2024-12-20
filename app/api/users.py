from fastapi import APIRouter, HTTPException
from app.models.users import UserCreate, UserAuth, UserResponse
from app.db.mongo import mongo_manager

router = APIRouter()
users_collection = mongo_manager.get_collection("users")

@router.post("/users")
def register_user(user: UserCreate):
    if users_collection.find_one({"username": user.user_id}):
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    new_user = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "access": user.access,
        "withdrawals": []
    }

    result = users_collection.insert_one(new_user)

    return {"message": "Usuario creado exitosamente", "id": str(result.inserted_id)}

@router.post("/users/auth")
def authenticate_user(auth_data: UserAuth):
    user = users_collection.find_one({"username": auth_data.username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Autenticación exitosa", "user": auth_data.username}

@router.get("/users", response_model=list[UserResponse])
def get_users():
    users = users_collection.find()
    users_list = [
        {
            "id": str(user["_id"]),
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "access": user["access"],
            "withdrawals": user["withdrawals"]
        }
        for user in users
    ]
    return users_list

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = users_collection.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} deleted successfully"}
