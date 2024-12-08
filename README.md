# Test Mekar Backend
[![codecov](https://codecov.io/gh/ghifariaulia/test-mekar-backend/graph/badge.svg?token=TJ1LN18MNE)](https://codecov.io/gh/ghifariaulia/test-mekar-backend)

This is the backend for the Test Mekar application, built using Django and Django REST Framework.

## Requirements

- Python 3.x
- Django
- Django REST Framework

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ghifariaulia/test-mekar-backend.git
    cd mekar-backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

- `GET /api/users/` - List all users (Needs Authentication)
- `POST /api/register/` - Register user
- `POST /api/login/` - Login user
- `POST /api/token/refresh/` - Refresh token

## Running Tests

To run the tests and show the coverage, use the following command:
1.  Run the test
    ```bash
    coverage run -m pytest
    ```
2.  Show the coverage
    ```bash
    coverage report
    ```
## Running Docker

You can use the run.sh script. Or use docker-compose manually.

## License

This project is licensed under the MIT License.
