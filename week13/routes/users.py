import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserUpdate
import json

router = APIRouter()

FILE_NAME = "users.txt"


def load_users():
    users = []

    if not os.path.exists(FILE_NAME):
        return users

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    users.append(json.loads(line))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    return users


def save_users(users):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for user in users:
                file.write(json.dumps(user) + "\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing file: {str(e)}")


def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1


@router.post("/", status_code=201)
def create_user(user: UserCreate):
    users = load_users()

    new_user = {
        "id": get_next_id(users),
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

    users.append(new_user)
    save_users(users)

    return {"message": "User created successfully!", "user": new_user}


@router.get("/")
def get_all_users():
    return load_users()


@router.get("/search")
def search_users(q: str):
    users = load_users()
    matches = [user for user in users if q.lower() in user["name"].lower()]
    return matches


@router.get("/{id}")
def get_user_by_id(id: int):
    users = load_users()

    for user in users:
        if user["id"] == id:
            return user

    raise HTTPException(status_code=404, detail="User not found!")


@router.put("/{id}")
def update_user(id: int, updated_user: UserCreate):
    users = load_users()

    for user in users:
        if user["id"] == id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            user["age"] = updated_user.age
            save_users(users)
            return {"message": "User updated successfully!", "user": user}

    raise HTTPException(status_code=404, detail="User not found!")


@router.delete("/{id}")
def delete_user(id: int):
    users = load_users()

    for user in users:
        if user["id"] == id:
            users.remove(user)
            save_users(users)
            return {"message": f"User {id} deleted successfully!"}

    raise HTTPException(status_code=404, detail="User not found!")