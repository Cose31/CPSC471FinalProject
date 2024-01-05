from flask import Flask
from flask_login import LoginManager, current_user

import os
import mysql.connector
from mysql.connector import Error
from database import create_server_connection

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Medical'

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        host = "localhost"
        user = "root"
        password = "bio"
        database = 'HOSPITAL'
        
        connection = create_server_connection(host, user, password, database)
        cursor = connection.cursor()

        cursor.execute("SELECT UserID, U_Role FROM user WHERE UserID = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            user_role, this_user = user_data
            return User(user_role, this_user)
        cursor.close()
        connection.close()
        return None
    

    return app
