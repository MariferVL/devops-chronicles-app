# DevOps Chronicles API

## Project Overview  
The **DevOps Chronicles API** is a practical, hands-on project designed to help DevOps enthusiasts master key technologies such as Flask, Docker, and Terraform. The API simulates a text-based adventure game where users manage heroes and track their progress as they overcome challenges like production outages, configuration drift, and pipeline failures. This updated version integrates automated AWS infrastructure provisioning via Terraform, Docker containerization, and a modular project structure for improved scalability and maintainability.
## Features

- **Heroes Management:**  
  - `POST /heroes/` – Create a new DevOps hero  
  - `GET /heroes/` – Retrieve all heroes  
  - `GET /heroes/<hero_id>` – Retrieve details for a specific hero  
  - `PUT /heroes/<hero_id>` – Update hero attributes  
  - `DELETE /heroes/<hero_id>` – Delete a DevOps hero

- **Adventures Management:**  
  - `POST /adventures/` – Initiate a new adventure challenge  
  - `GET /adventures/<adventure_id>` – View adventure details  
  - `GET /adventures/history` – Retrieve the log of all adventures

- **Infrastructure & Deployment:**  
  - **Terraform AWS Infrastructure:**  
    - Automated provisioning of an AWS RDS instance (MySQL 8.0), security groups, key pairs, and SSM parameters.
    - Uses a templated `init.sh.tpl` to inject environment variables into EC2 user_data.
  - **Docker Containerization:**  
    - Containerizes the Flask application for consistent, scalable deployments.
    - Updated Dockerfile and Docker Compose to match the new project structure.
  - **Project Reorganization:**  
    - Repository reorganized into three main directories: `app/`, `docker/`, and `terraform/`.
    - The Flask application is now modular, with code separated into its own `app/` directory.

## Tech Stack

- **Backend Framework:** Flask (Python 3)
- **Containerization:** Docker, Docker Compose
- **Cloud Infrastructure:** AWS RDS (provisioned via Terraform)
- **Database Migration:** Flask-Migrate (Alembic)
- **API Documentation:** Flasgger (Swagger UI) & hosted version on SwaggerHub
- **Production Server:** Gunicorn
- **Version Control:** Git

## Project Structure

```plaintext
devops-chronicles/
├── app/                  
│   ├── adventures/       # Adventure blueprints, models, and routes
│   ├── heroes/           # Hero blueprints, models, and routes
│   ├── migrations/       # Database migration scripts (generated via Flask-Migrate)
│   ├── __init__.py       # Main Flask application initializer
│   ├── app.py            # Main Flask application file
│   └── extensions.py     # Extensions (e.g., SQLAlchemy instance)
├── docker/               
│   ├── Dockerfile        # Docker image build instructions
│   └── docker-compose.yml # Docker Compose configuration
├── terraform/            
│   ├── init.sh.tpl       # Initialization script for Terraform
│   ├── main.tf           # Terraform configuration for AWS infrastructure
│   ├── terraform.tfvars  # Terraform variable definitions  (not committed)
│   └── variables.tf      # Terraform variables
├── swagger.yml           # External OpenAPI specification file  (not committed)
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation (this file)
├── .env                  # Environment variables (not committed)
├── .dockerignore         # Files to ignore in Docker builds
└── .gitignore            # Git ignore rules
```

## Installation

### Prerequisites
- Git, Docker, Docker Compose, Terraform, and Python 3 installed.
- An AWS account configured for Terraform deployments.

### 1. Clone the Repository

```bash
git clone https://github.com/MariferVL/devops-chronicles-app.git
cd devops-chronicles-app
```

### 2. Environment Variables Setup

Create a file named `.env` in the repository root and add the following content (replace placeholder values with your own configuration):

```dotenv
# .env file

# Flask settings
FLASK_APP=app/app.py
FLASK_ENV=development  # Change to production if necesary

# Database configuration
DB_HOST=db             # Use "db" when running in Docker and localhost in development
DB_USER=your_username  # Your database username 
DB_PASS=your_password  # Your database password
DB_NAME=your_db_name   # Your database name
```

### 3. Setting Up the Development Environment (Local)

#### a. Python Virtual Environment (for local development)

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate  
# On Linux/macOS:
source .venv/bin/activate
```

#### b. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Docker Setup

Build and run the Docker containers from the repository root:

```bash
docker-compose -f docker/docker-compose.yml --env-file .env up --build
```

This command uses the Dockerfile in the `docker/` directory to build the image and starts containers for the web application and MySQL database.
Below is a revised, neatly formatted "Database Migrations" section for your README:


### 5. Database Migrations

After the containers are running, perform the database migrations **inside the web container**. This ensures that Flask has access to your code and environment.

1. **Identify the container names:**

   Run:
   ```bash
   docker ps
   ```
   This lists all running containers. For example:
   - `docker-db-1` for the database container
   - `docker-web-1` for the web container  
   *(Note: Container names are auto-generated by Docker Compose and may vary on different machines.)*

2. **Enter the web container:**

   Use the container name from the previous step:
   ```bash
   docker exec -it docker-web-1 bash
   ```

3. **Run the migration commands inside the container:**

   Once inside, execute:
   ```bash
   flask db init         # (Only needed once; creates the 'migrations' folder.)
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Verify the tables in the database:**

   Exit the web container and connect to the database container:
   ```bash
   docker exec -it docker-db-1 mysql -u <DB_USER> -p
   ```
   Replace `<DB_USER>` with your database username.

   Then, in the MySQL prompt, run:
   ```sql
   USE <DB_NAME>;
   SHOW TABLES;
   ```
   Replace `<DB_NAME>` with your database name. This confirms that the tables have been created.

### 6. Terraform Infrastructure Setup

Provision your AWS infrastructure with Terraform:

1. Open a terminal and navigate to the `terraform/` directory:

   ```bash
   cd terraform
   ```

2. Initialize Terraform:

   ```bash
   terraform init
   ```

3. Generate and review the execution plan:

   ```bash
   terraform plan -out=tf_plan.out
   ```

4. Apply the plan to provision AWS resources:

   ```bash
   terraform apply tf_plan.out
   ```

## Running the Application

- **Development Mode (Local):**  
  Run the Flask application directly (outside Docker):

  ```bash
  python app/app.py
  ```
  
  The application will be available at [http://localhost:5000](http://localhost:5000).

- **Docker Mode:**  
  With the containers running via Docker Compose, access the application at [http://localhost:5000](http://localhost:5000).

- **Production Mode:**  
  In production, the application is served by Gunicorn within the container:

  ```bash
  gunicorn app:app --workers 4
  ```

## API Documentation

- **Local Swagger UI:**  
  Visit [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) for interactive API documentation.
- **Hosted Documentation:**  
  Alternatively, view the API docs on SwaggerHub at [SwaggerHub](https://app.swaggerhub.com/apis-docs/MARIFERVLDEV/dev-ops_chronicles_api/1.0.0).

## Contributing

Contributions, improvements, and suggestions are welcome!  
Fork the repository, make your changes according to the project's guidelines, and submit a pull request. Please include tests when applicable.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or further information, please visit my [GitHub profile](https://github.com/MariferVL).

