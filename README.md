# Gradex

## Technology Stack

- Frontend: React + TypeScript
- Backend: python
- Database: SQL Server

## TL;DR
Gradex is a smart system for automatically grading tests with open-ended questions. It combines a React + TypeScript frontend with a Python Flask backend, backed by SQL Server and a local SentenceTransformer model.

## Overview
Gradex provides a classroom API and a React frontend for managing subjects, classes, teachers, students, exams, questions, and answers. The backend uses Flask, SQLAlchemy, and a local sentence-transformers model for automated grading and similarity-based answer evaluation.

## Installation
1. Clone the repository.
2. Install frontend dependencies:
   ```bash
   cd client
   npm install
   ```
3. Install backend dependencies:
   ```bash
   cd ../server
   python -m pip install -r requirements.txt
   ```

> Note: The project is still in development and depends on local SQL Server configuration and the model stored in `server/my_model`.

## Running the project

### Backend
From the `server` folder:
```bash
python app.py
```
The Flask app runs on port `5000` in debug mode.

### Frontend
From the `client` folder:
```bash
npm run dev
```
This starts the Vite development server.

### Production / build
The frontend can be built with:
```bash
cd client
npm run build
```
The backend does not include a dedicated production deployment script. Use a WSGI server such as Gunicorn or a compatible environment for production deployment.

## Environment variables
### Client
Use Vite env vars to point the frontend at the backend:
```env
VITE_SERVER_URL=http://localhost:5000
```

### Server
The backend can read SQL Server settings from environment variables:
```env
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=GradexDB
DB_DRIVER=ODBC+Driver+17+for+SQL+Server
```

## Project structure overview

- `client/` — React + TypeScript + Vite frontend
- `server/` — Python Flask backend with SQLAlchemy, grading services, and local model assets

## Main features
- React + TypeScript frontend built with Vite
- Login form with `react-hook-form` and `zod` validation
- Flask REST API for educational entities and grading
- SQL Server persistence via SQLAlchemy and pyodbc
- Local sentence-transformers model loaded from `server/my_model`
- Modular backend design with controllers, repositories, and services

## Technical Details
- `server/app.py` is the Flask entrypoint and registers blueprints for subjects, classes, teachers, students, exams, questions, options, student answers, student exams, teacher answers, and question types.
- The backend loads a local SentenceTransformer model from `server/my_model` for grading operations.
- Database connection logic is implemented in `server/db_connection.py` and tested via `server/db_connection_test.py`.
- The backend currently starts with `app.run(debug=True, port=5000)`.
- Frontend backend URL configuration is exposed in `client/src/config.ts` via `import.meta.env.VITE_SERVER_URL`.
- The codebase includes tests under `server/tests/`, but production readiness is not yet established.
