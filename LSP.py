class UserService:
    def save_user(self, user):
        raise NotImplementedError

class AdminUserService(UserService):
    def save_user(self, user):
        # Save logic for admin user
        print("Saving admin user")

class RegularUserService(UserService):
    def save_user(self, user):
        # Save logic for regular user
        print("Saving regular user")

# Usage
def create_user(service: UserService, user_data):
    user = User(user_data['name'], user_data['email'])
    service.save_user(user)
    return "User created successfully"

# Both AdminUserService and RegularUserService can be used interchangeably
admin_service = AdminUserService()
regular_service = RegularUserService()
create_user(admin_service, {'name': 'Admin', 'email': 'admin@example.com'})
create_user(regular_service, {'name': 'User', 'email': 'user@example.com'})