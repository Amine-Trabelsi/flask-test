from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = 'RandomBIGStringHere'

    db.init_app(app)

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)
    
    app.debug =True
    
    return app
