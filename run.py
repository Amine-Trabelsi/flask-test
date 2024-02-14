from flask import Flask
from app import create_app, db

from app.models import User
app = create_app()

def create_database():
    with app.app_context():
        db.create_all()
        users_data = [
            {"username": "user1", "balance": 5000},
            {"username": "user2", "balance": 7500},
            {"username": "user3", "balance": 10000},
            {"username": "user4", "balance": 12500},
            {"username": "user5", "balance": 15000},
        ]
        for user_info in users_data:
            existing_user = User.query.filter_by(username=user_info["username"]).first()

            if not existing_user:
                new_user = User(username=user_info["username"], balance=user_info["balance"])
                db.session.add(new_user)
        db.session.commit()

create_database()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
