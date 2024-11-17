# Before: A large interface
class UserService:
    def create_user(self, data):
        pass
    def update_user(self, user_id, data):
        pass
    def delete_user(self, user_id):
        pass

# After: Segregated interfaces
class CreateUserService:
    def create_user(self, data):
        pass

class UpdateUserService:
    def update_user(self, user_id, data):
        pass

class DeleteUserService:
    def delete_user(self, user_id):
        pass

# Usage
create_service = CreateUserService()
create_service.create_user({'name': 'User', 'email': 'user@example.com'})