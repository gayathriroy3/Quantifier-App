import os
from flask import Flask
from application.database import db

app=None

def create_app():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    app=Flask(__name__,template_folder="templates")
    app.secret_key = 'super secret key'
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"db_directory/db.sqlite3")
    db.init_app(app)
    app.app_context().push()
    
    return app

app=create_app()

from application.controllers import *

if __name__=="__main__":
    app.run(debug=True)
