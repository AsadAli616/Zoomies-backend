from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from flask_mail import Mail

mongo = PyMongo()
jwt = JWTManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "super-secret-key"
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app) 
    from .db_init.collections import create_collections
    create_collections()
        
    # ✅ import blueprints from routes package
    from app.routes.routes import main
    from  app.routes.auth_routes import auth
    from app.routes.user_routes import users


    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(users, url_prefix="/users")

    return app
