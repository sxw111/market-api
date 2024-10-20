# Market API

API with `JWT` and `Google OAuth2` authentication, email verification during registration through the `hunter.io` service, and product management functions.

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Caching**: [Redis](https://redis.io/)
- **Containerization**: [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Validation and Serialization**: [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Asynchronous Programming**: Fully asynchronous implementation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sxw111/market-api.git
   cd market-api
   ```

2. Edit the `.env` file by adding your data.

3. Build and Run the Docker Containers:

   ```bash
   docker-compose up --build
   ```

4. Open your browser and go to http://localhost:8000/docs to view the Swagger documentation and interact with the API.
