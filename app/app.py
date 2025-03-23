import os
from flask import Flask, render_template
# from flasgger import Swagger
from dotenv import load_dotenv
from app.extensions import db
from app.heroes.routes import heroes_bp
from app.adventures.routes import adventures_bp
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db, directory='app/migrations')

# swagger = Swagger(app, template_file='swagger.yml')

app.register_blueprint(heroes_bp, url_prefix='/heroes')
app.register_blueprint(adventures_bp, url_prefix='/adventures')

@app.route('/')
def welcome():
    """
    Welcome endpoint for "DevOps Chronicles".
    """
    return render_template('index.html')

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'development':
        with app.app_context():
            from app.heroes.models import Hero  
            from app.adventures.models import Adventure 
            db.create_all()
    # For development, run with debug=True:
    #   python -m app.app

    # In production, run with Gunicorn (example):
    #   gunicorn app.app:app --workers 4
    app.run(debug=True)
