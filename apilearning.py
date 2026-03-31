from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdate
from typing import List
from uuid import uuid4, UUID

db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        role=[Role.user]
    ),
    User(
        id=uuid4(),
        first_name="Alexy",
        last_name="Dani",
        gender=Gender.female,
        role=[Role.admin, Role.user]
    )
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdate):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.role is not None:
                user.role = user_update.role
            return user
    raise HTTPException(status_code=404, detail="User not found")

