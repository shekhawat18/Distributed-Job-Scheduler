# Distributed Job Scheduler

A full-stack web application for managing distributed job processing with support for projects, queues, workers, scheduled jobs, retry policies, and a Dead Letter Queue (DLQ).

The project was built to demonstrate the core concepts behind modern background job processing systems. It provides a clean REST API using FastAPI and an interactive dashboard built with React for managing jobs throughout their lifecycle.

---

## Overview

Distributed systems often rely on background workers to execute tasks such as sending emails, generating reports, processing uploads, or communicating with external services. This project simulates that workflow by allowing jobs to be created, scheduled, retried on failure, and moved to a Dead Letter Queue once retry attempts are exhausted.

The application consists of two independent services:

- **Backend** built with FastAPI and PostgreSQL
- **Frontend** built with React, TypeScript, and Tailwind CSS

Authentication is handled using JWT, and all protected endpoints require a valid access token.

---

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected API routes

### Project Management

- Create projects
- View all projects
- Update project details
- Delete projects

### Queue Management

- Create queues
- Organize jobs into queues
- View queue information

### Job Management

- Create jobs
- Schedule jobs
- Update job status
- Delete jobs
- Retry failed jobs

### Worker Management

- Register workers
- Monitor worker status
- Track active workers

### Dashboard

- Project statistics
- Queue statistics
- Job statistics
- Worker overview
- Dead Letter Queue summary

### Retry Engine

- Configurable retry attempts
- Retry failed jobs
- Automatic retry handling

### Dead Letter Queue

- Store permanently failed jobs
- View failed jobs
- Retry jobs from the DLQ

---

## Technology Stack

### Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| Alembic | Database migrations |
| Pydantic | Request validation |
| JWT | Authentication |

### Frontend

| Technology | Purpose |
|------------|---------|
| React | UI |
| TypeScript | Type safety |
| Vite | Build tool |
| Tailwind CSS | Styling |
| Axios | API communication |

---

## High-Level Architecture

```text
                    React Frontend
                           │
                           │ HTTP + JWT
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    Authentication      Job APIs         Worker APIs
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                     Scheduler Service
                           │
                    Retry Management
                           │
                  Dead Letter Queue
                           │
                           ▼
                      PostgreSQL
```

---

## Project Structure

```
Distributed-Job-Scheduler
│
├── backend
│   ├── alembic
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── models
│   │   ├── schemas
│   │   ├── scheduler
│   │   ├── services
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── services
│   │   ├── lib
│   │   ├── types
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

## Application Workflow

The application follows a simple workflow for processing background jobs.

1. A user creates a project.
2. One or more queues are created within the project.
3. Jobs are submitted to a queue.
4. Workers pick pending jobs.
5. The scheduler tracks execution.
6. Failed jobs are retried according to the configured retry policy.
7. Jobs that exceed the retry limit are moved to the Dead Letter Queue.

This workflow reflects the architecture commonly used in distributed job processing systems.

---

## Current Modules

The project currently includes the following modules:

| Module | Status |
|----------|--------|
| Authentication | ✅ Complete |
| Projects | ✅ Complete |
| Queues | ✅ Complete |
| Jobs | ✅ Complete |
| Workers | ✅ Complete |
| Dashboard | ✅ Complete |
| Scheduler | ✅ Complete |
| Retry Engine | ✅ Complete |
| Dead Letter Queue | ✅ Complete |
| Swagger Documentation | ✅ Complete |

---## Getting Started

### Prerequisites

Before running the project, make sure the following software is installed on your machine.

- Python 3.10 or later
- Node.js 18 or later
- PostgreSQL
- Git

It is also recommended to use a virtual environment for the backend.

---

## Clone the Repository

```bash
git clone https://github.com/shekhawat18/Distributed-Job-Scheduler.git

cd Distributed-Job-Scheduler
```

---

# Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

### Create a Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/job_scheduler

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the database credentials with your own PostgreSQL configuration.

---

### Run Database Migrations

```bash
alembic upgrade head
```

This command creates all required database tables.

---

### Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The backend will start on:

```
http://localhost:8000
```

Swagger documentation is available at:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Open another terminal and navigate to the frontend folder.

```bash
cd frontend
```

---

### Install Dependencies

```bash
npm install
```

---

### Start the Development Server

```bash
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## Running the Application

After starting both services:

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

Open the frontend in your browser and log in to start managing projects, queues, jobs, and workers.

---

# API Overview

The backend exposes REST APIs for all major modules.

| Module | Description |
|----------|-------------|
| Authentication | User registration and login |
| Projects | CRUD operations for projects |
| Queues | Queue management |
| Jobs | Job scheduling and lifecycle management |
| Workers | Worker registration and monitoring |
| Dashboard | Aggregated statistics |
| Retry | Retry failed jobs |
| Dead Letter Queue | Manage permanently failed jobs |

All authenticated endpoints require a valid JWT access token.

---

## Authentication Flow

```
User Login
      │
      ▼
Validate Credentials
      │
      ▼
Generate JWT Token
      │
      ▼
Store Token
      │
      ▼
Include Token in Authorization Header
      │
      ▼
Access Protected Endpoints
```

---

## Job Processing Flow

```
Create Job
     │
     ▼
Pending
     │
     ▼
Worker Picks Job
     │
     ▼
Execute Job
     │
     ▼
Success?
 ┌────┴────┐
 │         │
Yes        No
 │         │
 ▼         ▼
Completed Retry Engine
             │
             ▼
     Retry Attempts Left?
        │
   ┌────┴────┐
   │         │
  Yes        No
   │         │
   ▼         ▼
 Retry     Dead Letter Queue
```

---

## Folder Overview

### Backend

```
app/
├── api/
│     Route definitions
│
├── core/
│     Configuration and authentication
│
├── db/
│     Database connection
│
├── models/
│     SQLAlchemy models
│
├── schemas/
│     Request and response schemas
│
├── scheduler/
│     Scheduling logic
│
├── services/
│     Business logic
│
└── main.py
      Application entry point
```

### Frontend

```
src/
├── components/
│     Reusable UI components
│
├── pages/
│     Application pages
│
├── services/
│     API service layer
│
├── types/
│     TypeScript interfaces
│
├── lib/
│     Axios configuration
│
└── App.tsx
```

---

## Design Decisions

A few decisions influenced the overall architecture of the project:

- FastAPI was chosen for its performance, automatic API documentation, and type validation.
- SQLAlchemy provides a clean ORM layer for interacting with PostgreSQL.
- Alembic is used to manage database schema changes.
- React with TypeScript offers a maintainable and scalable frontend.
- Tailwind CSS keeps styling simple while allowing rapid UI development.
- JWT authentication keeps the backend stateless and easy to integrate with different clients.

The project separates API routes, schemas, models, and business logic to keep the codebase modular and easier to extend.

---## Screenshots

The following screenshots show different parts of the application. Replace the placeholders with actual images from your project.

### Login

![Login](docs/images/login.png)

---

### Dashboard

![Dashboard](docs/images/dashboard.png)

---

### Projects

![Projects](docs/images/projects.png)

---

### Queues

![Queues](docs/images/queues.png)

---

### Jobs

![Jobs](docs/images/jobs.png)

---

### Workers

![Workers](docs/images/workers.png)

---

### Dead Letter Queue

![Dead Letter Queue](docs/images/dlq.png)

---

## Future Improvements

Although the application is fully functional, there are several areas that could be expanded in the future.

- Docker support for simplified deployment
- Redis for caching frequently accessed data
- RabbitMQ or Kafka for distributed message processing
- WebSocket support for real-time dashboard updates
- Role-Based Access Control (RBAC)
- Email and webhook notifications
- Job priorities and scheduling policies
- Advanced filtering and analytics
- Audit logging
- CI/CD pipeline using GitHub Actions
- Kubernetes deployment
- Prometheus and Grafana monitoring

---

## Known Limitations

This project was developed as a learning-focused implementation of a distributed job scheduling system. Some production-level features have intentionally been kept out of scope.

Current limitations include:

- Jobs are processed within the application rather than by distributed worker nodes.
- Horizontal scaling has not been implemented.
- No message broker such as RabbitMQ or Kafka is currently used.
- Live dashboard updates require page refreshes.
- No role-based authorization beyond user authentication.

These enhancements are planned as future improvements.

---

## What I Learned

Building this project provided hands-on experience with:

- Designing RESTful APIs using FastAPI
- Structuring a modular backend architecture
- Working with SQLAlchemy and Alembic migrations
- Implementing JWT-based authentication
- Managing relational data with PostgreSQL
- Building responsive interfaces with React and Tailwind CSS
- Organizing frontend API communication using Axios
- Understanding concepts such as job queues, retries, workers, and dead letter queues
- Integrating backend and frontend into a complete full-stack application

---

## Contributing

Contributions, suggestions, and improvements are always welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License.

Feel free to use the project for learning and educational purposes.

---

## Author

**Harsh Vardhan Shekhawat**

GitHub: https://github.com/shekhawat18

LinkedIn: *(Add your LinkedIn profile here)*

Email: *(Add your email address here)*

---

## Acknowledgements

This project was developed as part of my learning journey in backend development, distributed systems, and full-stack application development.

Special thanks to the FastAPI, React, SQLAlchemy, PostgreSQL, and Tailwind CSS communities for their excellent documentation and open-source contributions.

---

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.

Feedback and suggestions are always appreciated.