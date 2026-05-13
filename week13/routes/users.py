import json
import os
from fastapi import APIRouter, HTTPException, Query
from schema import User, UserCreate

router = APIRouter()

USERS_FILE = "users.json"


def read_users() -> list[dict]:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def write_users(users: list[dict]) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def get_next_id(users: list[dict]) -> int:
    if not users:
        return 1
    return max(u["id"] for u in users) + 1



@router.get("/search")
def search_users(q: str = Query(..., description="Search term for user name")):
    users = read_users()
    results = [u for u in users if q.lower() in u["name"].lower()]
    return results


@router.get("/")
def get_all_users():
    return read_users()


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail=f"User with id {user_id} is not found")


@router.post("/", status_code=201)
def create_user(user_data: UserCreate):
    users = read_users()
    new_user = {
        "id": get_next_id(users),
        "name": user_data.name,
        "age": user_data.age,
    }
    users.append(new_user)
    write_users(users)
    return new_user


@router.put("/{user_id}")
def update_user(user_id: int, user_data: UserCreate):
    users = read_users()
    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i] = {"id": user_id, "name": user_data.name, "age": user_data.age}
            write_users(users)
            return users[i]
    raise HTTPException(status_code=404, detail=f"User with id {user_id} is not found")


@router.delete("/{user_id}")
def delete_user(user_id: int):
    users = read_users()
    updated_users = [u for u in users if u["id"] != user_id]
    if len(updated_users) == len(users):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} is not found")
    write_users(updated_users)
    return {"message": f"User {user_id} is deleted successfully!"}