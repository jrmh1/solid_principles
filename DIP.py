class UserRepository:
    def save(self, user):
        raise NotImplementedError

class SqliteUserRepository(UserRepository):
    def save(self, user):
        print(f"Saving user {user.name} to SQLite database")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def save_user(self, user):
        self.repository.save(user)

# Usage
repository = SqliteUserRepository()
user_service = UserService(repository)
user_service.save_user(User('John', 'john@example.com'))