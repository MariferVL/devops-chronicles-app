# DevOps Chronicles API

## Project Overview
The **DevOps Chronicles API** is an educational project that simulates a humorous text-based adventure game for DevOps enthusiasts. This API allows users to manage heroes and send them on adventures that reflect common challenges in the DevOps realm, such as production outages, configuration drift, or pipeline meltdowns.

## Features
- **Hero Management:**  
  - `POST /hero/` - Create a new DevOps hero  
  - `GET /hero/<hero_id>` - Retrieve hero details  
  - `PUT /hero/<hero_id>` - Update hero attributes  
  - `DELETE /hero/<hero_id>` - Delete a DevOps hero
  
- **Adventure Management:**  
  - `POST /adventure/` - Initiate a new adventure challenge  
  - `GET /adventure/<adventure_id>` - View adventure details  
  - `GET /adventure/history` - Retrieve the log of all adventures
  
- **Interactive Documentation:**  
  The API documentation is available in two formats:
  - **Local Swagger UI:** Accessible at `/apidocs/` when running the application locally.
  - **Hosted on SwaggerHub:** View the hosted version of the API documentation at [SwaggerHub](https://app.swaggerhub.com/apis-docs/MARIFERVLDEV/dev-ops_chronicles_api/1.0.0).

## Tech Stack
- **Backend Framework:** Flask (Python 3)
- **API Documentation:** Flasgger (Swagger UI)
- **Production Server:** Gunicorn (optional for production deployments)
- **Version Control:** Git

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MariferVL/devops-diaries.git
   cd homeworks/devops-chronicles
   ```
   > **Note:** This project is part of a larger repository containing multiple homework projects.

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Linux use: source .venv/bin/activate
   ```

3. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
- **Development Mode:**  
  Run the Flask development server:
  ```bash
  python app.py
  ```
  The application will be available at `http://localhost:5000`.

- **Production Mode:**  
  Use Gunicorn to run the application:
  ```bash
  gunicorn app:app --workers 4
  ```

## API Documentation
Once the application is running:
- **Local Documentation:**  
  Access the interactive Swagger UI at [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/).

- **Hosted Documentation:**  
  Alternatively, view the API documentation on SwaggerHub at [SwaggerHub](https://app.swaggerhub.com/apis-docs/MARIFERVLDEV/dev-ops_chronicles_api/1.0.0).

## Project Structure
```
devops-chronicles/
├── app.py               # Main application file that registers blueprints and Swagger configuration
├── heroes.py            # Blueprint for managing DevOps heroes
├── adventures.py        # Blueprint for managing adventures and challenges
├── swagger.yml          # External OpenAPI specification file (documentation)
├── requirements.txt     # Project dependencies
├── README.md            # This documentation file
└── .gitignore           # Git ignore rules
```

## Contributing
This project is intended for educational purposes. Contributions, improvements, and suggestions are welcome. Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any questions or further information, please visit my [GitHub profile](https://github.com/MariferVL).
