import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas import UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException
from user_store import UserStore

router = APIRouter()

store = UserStore('users.db')


@router.post('/', status_code=201)
def create_user(user: UserCreate):
    new_user = {
        'name':  user.name,
        'email': user.email,
        'age':   user.age
    }
    user_id = store.save(new_user)
    new_user['id'] = user_id
    return {'message': 'User created successfully!', 'user': new_user}


@router.get('/')
def get_all_users():
    return store.load()


@router.get('/search')
def search_users(q: str):
    return store.search_users(q)


@router.get('/{user_id}')
def get_user_by_id(user_id: int):
    user = store.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found!')
    return user


@router.put('/{user_id}')
def update_user(user_id: int, updated: UserCreate):
    updated_data = {
        'name':  updated.name,
        'email': updated.email,
        'age':   updated.age
    }
    success = store.update_user(user_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail='User not found!')
    return {'message': 'User updated successfully!'}


@router.delete('/{user_id}')
def delete_user(user_id: int):
    success = store.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail='User not found!')
    return {'message': f'User {user_id} deleted successfully!'}
