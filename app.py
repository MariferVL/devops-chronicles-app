import os
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from extensions import db
from heroes.routes import heroes_bp
from adventures.routes import adventures_bp
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

swagger = Swagger(app, template_file='swagger.yml')

app.register_blueprint(heroes_bp, url_prefix='/heroes')
app.register_blueprint(adventures_bp, url_prefix='/adventures')

@app.route('/')
def welcome():
    """
    Welcome endpoint for "DevOps Chronicles".
    """
    return """
    <h1>Welcome to The DevOps Chronicles</h1>
    <p>Your journey in automating chaos and bringing order to the digital realm begins now!</p>
    <ul>
      <li>POST /hero/ - Create a new DevOps hero</li>
      <li>GET /hero/&lt;hero_id&gt; - Retrieve hero details</li>
      <li>PUT /hero/&lt;hero_id&gt; - Update hero attributes</li>
      <li>DELETE /hero/&lt;hero_id&gt; - Delete a DevOps hero</li>
      <li>POST /adventure/ - Initiate a new adventure challenge</li>
      <li>GET /adventure/&lt;adventure_id&gt; - View adventure details</li>
      <li>GET /adventure/history - See the log of all adventures</li>
    </ul>
    """

if __name__ == '__main__':
    with app.app_context():
      from heroes.models import Hero  
      from adventures.models import Adventure 
      db.create_all()
    # For development, run with debug=True.
    # In production, run with Gunicorn (example):
    #   gunicorn app:app --workers 4
    app.run(debug=True)
