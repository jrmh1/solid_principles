# Before: Controller handling business logic
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    if not user.is_valid():
        return jsonify({'error': 'Invalid data'}), 400
    user.save()
    return jsonify({'message': 'User created successfully'}), 201

# After: Separation of concerns
class UserService:
    def create_user(self, data):
        user = User(name=data['name'], email=data['email'])
        if not user.is_valid():
            raise ValueError('Invalid data')
        user.save()
        return user

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user_service = UserService()
        user = user_service.create_user(data)
        return jsonify({'message': 'User created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400