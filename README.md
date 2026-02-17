## Running the Project with Docker

This project provides a Docker-based setup for local development and deployment. Below are the key details and instructions specific to this project:

### Project-Specific Docker Requirements
- **Python Version:** The Dockerfile uses `python:3.13-slim` as the base image.
- **System Dependencies:** Installs build tools and libraries required for Python packages (e.g., `libpq-dev`, `gcc`, `libffi-dev`, `libssl-dev`).
- **Non-root User:** The container runs as a non-root user (`appuser`) for improved security.

### Environment Variables
- The Docker Compose file supports an `.env` file at the project root (see `.env.example` for reference). Uncomment the `env_file` line in `docker-compose.yml` if you wish to use it:
  ```yaml
  env_file: ../.env
  ```
- Ensure all required environment variables are set in your `.env` file before running the containers.

### Build and Run Instructions
1. **Build and Start the Services:**
   From the project root, run:
   ```sh
   docker compose up --build
   ```
   This will build the image from the `./src` directory using the root-level `Dockerfile` and start the `python-src` service.

2. **Access the Application:**
   - The Django app will be available at [http://localhost:8000](http://localhost:8000).

### Ports
- **python-src:** Exposes port `8000` (default for Django's development server).

### Special Configuration
- If your application requires a database (e.g., PostgreSQL), you can add the service to `docker-compose.yml` (see the commented example in the file) and configure the appropriate environment variables in your `.env` file.
- The Dockerfile is set up to run `python manage.py runserver 0.0.0.0:8000` by default. Adjust the `CMD` in the Dockerfile if you need to use a different WSGI server (e.g., Gunicorn) for production.

---

_Keep your `.env` file up to date with all required settings. For more details, refer to the `.env.example` file._
