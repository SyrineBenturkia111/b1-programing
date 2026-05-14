import json
import os

class UserStore:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [json.loads(line) for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def save(self, users):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for user in users:
                file.write(json.dumps(user) + "\n")

    def find_by_id(self, user_id):
        users = self.load()
        for user in users:
            if user.get('id') == user_id:
                return user
        return None

    def update_user(self, user_id, updated_data):
        users = self.load()
        for user in users:
            if user.get('id') == user_id:
                user.update(updated_data)
                self.save(users)
                return True
        return False

    def delete_user(self, user_id):
        users = self.load()
        filtered = [user for user in users if user.get('id') != user_id]
        if len(filtered) == len(users):
            return False
        self.save(filtered)
        return True
