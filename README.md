# Voting API Project

This project is a Django-based application that allows users to vote for restaurants. It leverages Django REST Framework for API management, PostgreSQL as the main database, and Celery for handling periodic tasks related to voting management. The system is designed to manage voting operations efficiently and include features such as vote locking and daily winner calculation.

---

## Project Setup

### Prerequisites

The project requires the dependencies listed in `requirements.txt`. These include:

- Django
- Django REST Framework
- Celery
- PostgreSQL
- pytest
- mypy
- flake8
- pylint

These dependencies will be installed automatically when the Docker container is built.

### Running the Project

The project is designed to run using Docker, which will set up the Django application, PostgreSQL, and any other necessary services. The application will automatically apply any pending migrations and set up periodic tasks.

`docker-compose up`

## API Endpoints

### User Authentication

- **Create User**
  - `POST /auth/users/`
  - Request Body: `{ "username": "string", "password": "string", "email": "string" }`
  - Response: `201 Created` or `400 Bad Request`

- **Create JWT**
  - `POST /auth/jwt/create/`
  - Request Body: `{ "username": "string", "password": "string" }`
  - Response: `200 OK` or `400 Bad Request`

### Restaurant Endpoints

- **Create Restaurant**
  - `POST /restaurant/`
  - Request Body: `{ "name": "string" }`
  - Response: `201 Created` or `400 Bad Request`

- **Retrieve Restaurant by ID**
  - `GET /restaurant/{id}/`
  - Response: `200 OK` or `404 Not Found`

- **List Restaurants**
  - `GET /restaurant/`
  - Response: `200 OK`

- **Update Restaurant**
  - `PUT/PATCH /restaurant/{id}/`
  - Request Body: `{ "name": "string" }`
  - Response: `200 OK` or `400 Bad Request`

- **Delete Restaurant**
  - `DELETE /restaurant/{id}/`
  - Response: `204 No Content` or `404 Not Found`

### Voting Endpoints

- **Create Vote**
  - `POST /voting/`
  - Request Body: `{ "restaurant_id": int }`
  - Response: `201 Created` or `423 Locked`

### Voting History Endpoints

- **Retrieve Voting History**
  - `GET /voting-history/`
  - Response: `200 OK`

- **Filter Voting History by Date Range**
  - `POST /voting-history/`
  - Request Body: `{ "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "restaurants": "comma-separated-ids" }`
  - Response: `200 OK` or `400 Bad Request`



## Timer Management and Periodic Tasks

- **Daily Winner Calculation**
  - Triggered daily to determine the top restaurant based on votes.
  - Automatically managed by a periodic Celery task.

- **Vote Locking**
  - Votes can be locked or unlocked based on specific conditions.
  - Managed via the `VotingLocker` model with API endpoints to lock or unlock voting.

## Testing

To ensure everything is working correctly, run the provided unit tests. Tests cover API functionality, voting logic, and periodic task execution.

1. **Testing and Code Validation:**

   To run the tests and validate the code, use the following command: `docker-compose run --rm app sh -c "pytest && mypy . && flake8"`

   This command runs:

   - pytest for running the unit tests.
   - mypy for type checking.
   - flake8 for linting the code according to PEP 8 standards.
   - pylint for code quality checks.

   The project includes various tests to validate functionality and code quality. These tests cover:

   - Creation and validation of votes
   - Handling vote locking
   - Retrieval and deletion of votes
   - Handling unsupported HTTP methods
   - Periodic task execution

### Unit Tests Overview

- **Vote API Tests**
  - `test_create_voting_returns_201`: Validates successful creation of a vote.
  - `test_unlock_voting_returns_201`: Ensures vote creation when voting is unlocked.
  - `test_create_voting_returns_400`: Handles requests with invalid input.
  - `test_list_voting_returns_405`: Handles requests with invalid HTTP method.
  - `test_calculate_daily_winner`: Ensures that the winner is calculated daily.
  - `test_delete_restaurant_return_204`: Validates successful deletion of a restaurant.
  - `test_create_voting_returns_401`: Ensures anonymous voting is not allowed.

- **Celery Task Tests**
  - `test_calculate_daily_winner`: Validates successful daily winner calculation.
  - `test_lock_voting_multiple_dates_returns_403`: Ensures no calculations are performed if there are votes from different dates.
  - `test_lock_voting_task`: Validates functionality of the vote locking task.
  - `test_unlock_voting_returns_201`: Ensures that the lock is released.
