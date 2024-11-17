# Activity 33: SOLID PRINCIPLES
# 1. Single Responsibility Principle (SRP)
Definition:
The Single Responsibility Principle states that a class should have only one reason to change, meaning it should have only one job or responsibility. This helps make code more modular and reduces complexity.

Application in Flask:
In Flask applications, controllers (views or route handlers) should ideally only handle the request-response cycle. Business logic or data processing should be separated into different services or models.

Code Example:
 Before: Controller handling business logic
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    if not user.is_valid():
        return jsonify({'error': 'Invalid data'}), 400
    user.save()
    return jsonify({'message': 'User created successfully'}), 201

 After: Separation of concerns
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
        
Explanation:
In the first example, the Flask route handles both the HTTP request and business logic. After refactoring, we move the business logic into a separate UserService class, which is responsible for user creation, while the route only deals with the HTTP request and response.

# 2. Open/Closed Principle (OCP)
Definition:
The Open/Closed Principle states that software entities (classes, modules, functions) should be open for extension but closed for modification. This means that you should be able to add new functionality without changing the existing code.

Application in Flask:
In Flask, this can be achieved by using inheritance or composition to extend functionality without modifying existing route handlers or services.

Code Example:

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


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_type = data.get('role', 'regular')
    creator = AdminUserCreator() if user_type == 'admin' else RegularUserCreator()
    user = creator.create(data)
    return jsonify({'message': f'{user.role.capitalize()} user created successfully'}), 201
    
Explanation:
In the example above, the UserCreator class is open for extension (we can create new user creation strategies like AdminUserCreator or RegularUserCreator), but closed for modification (we don't need to change the original create_user route logic).

# 3. Liskov Substitution Principle (LSP)
Definition:
The Liskov Substitution Principle states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program. This means subclasses must behave in a way that the parent class does.

Application in Flask:
In Flask, LSP can be maintained by ensuring that subclasses or overridden methods behave as expected without breaking the core functionality of the application.

Code Example:

class UserService:
    def save_user(self, user):
        raise NotImplementedError

class AdminUserService(UserService):
    def save_user(self, user):
    
        print("Saving admin user")

class RegularUserService(UserService):
    def save_user(self, user):
    
        print("Saving regular user")


def create_user(service: UserService, user_data):
    user = User(user_data['name'], user_data['email'])
    service.save_user(user)
    return "User created successfully"


admin_service = AdminUserService()
regular_service = RegularUserService()
create_user(admin_service, {'name': 'Admin', 'email': 'admin@example.com'})
create_user(regular_service, {'name': 'User', 'email': 'user@example.com'})

Explanation:
The UserService class defines the contract, and both AdminUserService and RegularUserService respect that contract, allowing substitution without affecting the correctness of user creation.

# 4. Interface Segregation Principle (ISP)
Definition:
The Interface Segregation Principle suggests that clients should not be forced to depend on interfaces they do not use. This means splitting large, monolithic interfaces into smaller, more specific ones.

Application in Flask:
In Flask, ISP can be applied by splitting complex services or interfaces into smaller, more focused services that only expose the functionality required by the consumer.

Code Example:

class UserService:
    def create_user(self, data):
        pass
    def update_user(self, user_id, data):
        pass
    def delete_user(self, user_id):
        pass


class CreateUserService:
    def create_user(self, data):
        pass

class UpdateUserService:
    def update_user(self, user_id, data):
        pass

class DeleteUserService:
    def delete_user(self, user_id):
        pass


create_service = CreateUserService()
create_service.create_user({'name': 'User', 'email': 'user@example.com'})

Explanation:
By separating the responsibilities into smaller, more focused classes, we ensure that clients are only dependent on the interfaces they actually need, making the code easier to understand and maintain.

# 5. Dependency Inversion Principle (DIP)
Definition:
The Dependency Inversion Principle states that high-level modules should not depend on low-level modules. Both should depend on abstractions (e.g., interfaces or abstract classes). Furthermore, abstractions should not depend on details; details should depend on abstractions.

Application in Flask:
In Flask, DIP can be implemented by using dependency injection and ensuring that higher-level components depend on abstractions, not concrete implementations.

Code Example:


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


repository = SqliteUserRepository()
user_service = UserService(repository)
user_service.save_user(User('John', 'john@example.com'))

Explanation:
By introducing an abstraction (UserRepository), we allow the UserService to be decoupled from specific database implementations, making it easy to swap out repositories without modifying the business logic.

# Real-World Use Cases
1. E-Commerce Platform
In an e-commerce platform, you might have different user roles (admin, customer, guest), and each might require different behavior. Using the Open/Closed Principle allows you to extend functionality (e.g., adding a new user type) without changing the existing code.

2. Microservices Architecture
In a microservices-based application, using Dependency Injection (as per DIP) helps you inject dependencies such as database connections or APIs into services, making each service testable and decoupled from concrete implementations.

3. Web APIs
In a Flask API, following SRP and ISP can help keep your route handlers thin by delegating business logic to specialized services, making your API endpoints more maintainable.

https://kmjrmh.hashnode.dev/activity-33-solid-principles

https://en.wikipedia.org/wiki/SOLID
