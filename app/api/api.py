from fastapi import FastAPI
from models.users import router as users_router
from models.inventory import router as inventory_router
from models.withdrawals import router as withdrawals_router
from db.mongo import mongo_manager

app = FastAPI()

app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(withdrawals_router, prefix="/api/withdrawals", tags=["Withdrawals"])

@app.on_event("startup")
def startup_event():
    mongo_manager.connect()

@app.on_event("shutdown")
def shutdown_event():
    mongo_manager.close()


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)