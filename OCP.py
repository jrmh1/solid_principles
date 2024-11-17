# Base class for creating a user
class UserCreator:
    def create(self, data):
        raise NotImplementedError("Subclasses should implement this method")

class AdminUserCreator(UserCreator):
    def create(self, data):
        user = User(name=data['name'], email=data['email'], role='admin')
        user.save()
        return user

class RegularUserCreator(UserCreator):
    def create(self, data):
        user = User(name=data['name'], email=data['email'], role='regular')
        user.save()
        return user

# Route to create a user with different roles
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_type = data.get('role', 'regular')
    creator = AdminUserCreator() if user_type == 'admin' else RegularUserCreator()
    user = creator.create(data)
    return jsonify({'message': f'{user.role.capitalize()} user created successfully'}), 201