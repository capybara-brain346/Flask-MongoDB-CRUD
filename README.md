# Flask Application with MongoDB - Dockerized Setup

## Overview

This project is a Flask-based backend application connected to a MongoDB database. It provides REST API endpoints for CRUD operations on `User` resources. The setup is containerized using Docker, ensuring consistency and ease of deployment.

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
git clone https://github.com/capybara-brain346/Flask-MongoDB-CRUD
cd Flask-MongoDB-CRUD
```

---

### **2. Build and Run the Application**

Use Docker Compose to build and start the services:

```bash
docker-compose up --build
```

---

### **3. Access the Application**

- **API Endpoints**: Visit `http://localhost:5000/users`.
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

## Scaling the Application

To scale the backend:

```bash
docker-compose up --scale flask-backend=3
```

For production, we can use a load balancer (e.g., NGINX) to distribute traffic.

---
