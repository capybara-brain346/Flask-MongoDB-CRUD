# Flask Application with MongoDB - Dockerized Setup

## Overview

This project is a Flask-based backend application connected to a MongoDB database. It provides REST API endpoints for CRUD operations on `User` resources. The setup is containerized using Docker, ensuring consistency and ease of deployment.

---

## Features

- **Flask Backend**:

  - REST API for CRUD operations.
  - Middleware for error handling, content-type validation, and CORS.
  - Uses Gunicorn for production-level WSGI serving.

- **MongoDB**:

  - Database for storing user data.
  - Initialized with user authentication and collections setup.

- **Dockerized Deployment**:
  - Containerized Flask and MongoDB.
  - Uses Docker Compose for orchestration.

---

## Prerequisites

- [Docker](https://www.docker.com/) (v20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/) (v1.29 or later)

---

## Directory Structure

```plaintext
project-root/
├── api/
│   ├── app.py                # Flask app entry point
│   ├── middleware.py         # Middleware implementations
│   ├── routes.py             # API routes
│   ├── requirements.txt      # Python dependencies
│   ├── wsgi.py               # Gunicorn entry point
│   └── Dockerfile            # Dockerfile for Flask app
├── mongo-init/
│   ├── init.js               # MongoDB initialization script
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # Project documentation
```

---

## Setup Instructions

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/flask-mongo-docker.git
cd flask-mongo-docker
```

---

### **2. MongoDB Initialization**

Ensure your MongoDB initialization script (`mongo-init/init.js`) contains:

```javascript
db.createUser({
  user: "appuser",
  pwd: "securepassword",
  roles: [{ role: "readWrite", db: "mydatabase" }],
});
db.createCollection("users");
```

This script will set up a database named `mydatabase`, a user with the `readWrite` role, and the `users` collection.

---

### **3. Build and Run the Application**

Use Docker Compose to build and start the services:

```bash
docker-compose up --build
```

---

### **4. Access the Application**

- **API Endpoints**: Visit `http://localhost:5000`.
- **MongoDB**: Connect via `mongodb://localhost:27017`.

---

## Services Overview

| Service         | Description                            | Port    |
| --------------- | -------------------------------------- | ------- |
| `flask-backend` | Flask application serving the REST API | `5000`  |
| `mongodb`       | MongoDB database for user data         | `27017` |

---

## Development Workflow

### **1. Modify Flask Code**

- Edit files in the `api/` directory.
- Restart the application for changes to take effect:
  ```bash
  docker-compose restart flask-backend
  ```

### **2. Debugging Logs**

View logs for the Flask backend:

```bash
docker-compose logs -f flask-backend
```

---

## Production Deployment

1. Update the Dockerfile to run in production mode:
   ```bash
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
   ```
2. Adjust `docker-compose.yml`:
   - Use robust logging and monitoring tools.
   - Enable health checks for services.
3. Deploy to a cloud provider using Docker Swarm, AWS ECS, or Kubernetes.

---

## Health Checks

- **Flask Backend**:
  - Add a `/health` endpoint to check service health.
  - Example: `curl http://localhost:5000/health`
- **MongoDB**:
  - Use the MongoDB client:
    ```bash
    mongo --eval "db.stats()"
    ```

---

## Common Issues

### **1. Port Conflicts**

If ports `5000` or `27017` are in use, modify `docker-compose.yml`:

```yaml
ports:
  - "new_port:5000" # Flask
  - "new_port:27017" # MongoDB
```

### **2. MongoDB Initialization Errors**

Ensure the `init.js` script runs on first start. Remove the volume and restart:

```bash
docker-compose down -v
docker-compose up --build
```

---

## Scaling the Application

To scale the backend:

```bash
docker-compose up --scale flask-backend=3
```

For production, use a load balancer (e.g., NGINX) to distribute traffic.

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---
