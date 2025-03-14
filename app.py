from flask import Flask
from flasgger import Swagger
from heroes import heroes_bp
from adventures import adventures_bp

app = Flask(__name__)

swagger = Swagger(app, template_file='swagger.yml')

# Register Blueprints on specific URL prefixes
app.register_blueprint(heroes_bp, url_prefix='/hero')
app.register_blueprint(adventures_bp, url_prefix='/adventure')

@app.route('/')
def welcome():
    """
    Welcome endpoint for "DevOps Chronicles" — where deployments misbehave.
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
    # For development, run with debug=True.
    # In production, run with Gunicorn (example):
    #   gunicorn app:app --workers 4
    app.run(debug=True)
