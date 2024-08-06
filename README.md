# Chatting

This repository contains a real-time chatting application built using FastAPI for the backend and React.js for the frontend. The application leverages WebSockets for real-time communication between the frontend and backend. The main focus of this project is its CI/CD workflow, utilizing Docker and Kubernetes for containerization and orchestration.

## Table of Contents
- Introduction
- Features
- Architecture
- CI/CD Workflow
- Contributing


## Introduction
The Chatting application is designed to facilitate real-time communication between users. The backend is built with FastAPI and utilizes WebSockets to handle chat messages efficiently. The frontend is developed using HTML, CSS, and React.js for a responsive and interactive user interface.

## Features
- Real-time messaging using WebSockets
- Responsive frontend built with React.js
- CI/CD pipeline for automated deployment
- Containerization with Docker
- Orchestration with Kubernetes

## Architecture
The application consists of the following components:

- Backend: FastAPI application with WebSocket support.
- Frontend: React.js application with a responsive chat interface.
- Docker: Separate Dockerfiles for backend and frontend.
- Kubernetes: Configuration for deploying the application.
- CI/CD Workflow: Automated deployment pipeline.

## CI/CD Workflow
The CI/CD pipeline is configured to automate the build, test, and deployment processes. The pipeline uses GitHub Actions for continuous integration and deployment. The configuration files are:
.github/workflows/ci-cd.yml: Defines the CI/CD workflow for the project.

## Contributing
Contributions are welcome! Please submit a Pull Request or open an Issue to suggest improvements.

