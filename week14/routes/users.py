from fastapi import APIRouter, HTTPException
from schema import UserCreate, UserUpdate
from user_store import UserStore

router = APIRouter()

store = UserStore("users.txt")


def get_next_id(users):
    if not users:
        return 1
    return max(user['id'] for user in users) + 1


@router.post("/", status_code=201)
def create_user(user: UserCreate):
    users = store.load()
    new_user = {
        'id': get_next_id(users),
        'name': user.name,
        'email': user.email,
        'age': user.age
    }
    users.append(new_user)
    store.save(users)
    return {'message': 'User created successfully!', 'user': new_user}


@router.get("/")
def get_all_users():
    return store.load()


@router.get("/search")
def search_users(q: str):
    users = store.load()
    return [user for user in users if q.lower() in user['name'].lower()]


@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    user = store.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found!')
    return user


@router.put("/{user_id}")
def update_user(user_id: int, updated: UserCreate):
    updated_data = {
        'name': updated.name,
        'email': updated.email,
        'age': updated.age
    }
    success = store.update_user(user_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail='User not found!')
    return {'message': 'User updated successfully!'}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    success = store.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail='User not found!')
    return {'message': f'User {user_id} deleted successfully!'}
