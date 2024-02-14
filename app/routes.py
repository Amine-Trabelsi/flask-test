from flask import request, Blueprint, current_app, jsonify
from app import db
from .models import User
from .views import Homepage
from .weather import WeatherAPI
from .forms import UserForm

main_blueprint = Blueprint('main', __name__)

# Homepage route to display user data
@main_blueprint.route('/')
def homepage():
    users = User.query.all()
    return Homepage().render(users)

# Api endpoint to update the balance of an User using a temperature of some city
# form data: user_id, city
@main_blueprint.route('/update_balance', methods=['POST'])
def update_balance():
    try:
        user_id = request.form.get('user_id')
        city = request.form.get('city')

        # Fetch the current temperature in the city
        weather_api = WeatherAPI()
        temperature = weather_api.fetch_weather(city)

        if temperature is not None:
            # Update the balance of the specified user based on temperature
            with current_app.app_context():
                user = User.query.get(user_id)

                if user:
                    new_balance = user.balance + temperature
                    user.balance = max(0, new_balance)

                    db.session.commit()

                    return f"User balance for user {user_id} updated based on {temperature}°C temperature in {city}."
                else:
                    return f"User with ID {user_id} not found."

            return f"User balances updated based on {temperature}°C temperature in {city}."
        else:
            return "Failed to fetch weather data."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Api endpoint to create, read, update, and delete Users 
@main_blueprint.route('/manage_users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_users():
    try:
        if request.method == 'GET':
            # Get all users
            with current_app.app_context():
                users = User.query.all()
                users_data = [{'id': user.id, 'username': user.username, 'balance': user.balance} for user in users]
                return jsonify({'users': users_data})

        elif request.method == 'POST':
            # Add a new user
            username = request.form.get('username')
            balance = float(request.form.get('balance'))

            with current_app.app_context():
                new_user = User(username=username, balance=balance)
                db.session.add(new_user)
                db.session.commit()

            return jsonify({'message': 'User added successfully'})

        elif request.method == 'PUT':
            # Update user balance
            user_id = int(request.form.get('user_id'))
            new_balance = float(request.form.get('balance'))

            with current_app.app_context():
                user = User.query.get(user_id)
                if user:
                    user.balance = new_balance
                    db.session.commit()
                    return jsonify({'message': f'Balance for user {user_id} updated successfully'})
                else:
                    return jsonify({'error': f'User with ID {user_id} not found'})

        elif request.method == 'DELETE':
            # Delete a user
            user_id = int(request.form.get('user_id'))

            with current_app.app_context():
                user = User.query.get(user_id)
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return jsonify({'message': f'User {user_id} deleted successfully'})
                else:
                    return jsonify({'error': f'User with ID {user_id} not found'})

        else:
            return jsonify({'error': 'Invalid HTTP method'})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})