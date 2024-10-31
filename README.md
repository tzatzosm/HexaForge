# HexaForge

## Introduction to Microservices

Microservices architecture is a design pattern that structures an application as a collection of loosely coupled services. Each service is fine-grained and performs a single function, which allows for better modularity, scalability, and maintainability. 

However, bootstrapping a new microservice project can be tedious, involving the setup of various libraries, frameworks, and tools.

## Project Description
HexaForge is an opinionated Spring Boot project generator.

- Gradle
- Hexagonal architecture
- [jib-gradle-plugin](https://github.com/GoogleContainerTools/jib/tree/master/jib-gradle-plugin#quickstart) for containerising your application

## Prerequisites
Before you begin, ensure you have the following tools installed:
- [Jinja2](https://jinja.palletsprojects.com/en/stable/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Generating your project

1. **Clone the repository**:
  ```sh
  git clone https://github.com/yourusername/hexaforge.git
  cd hexaforge
  ```

2. **Run the python script**:
  ```python
  ./generate.py
  ```

Open the generated project with your favorite IDE and your are good to go.

## Building the Project with Jib
Jib is a tool that helps you build optimized Docker and OCI images for your Java applications. Follow these steps to build the project:

1. **Clone the repository**:
  ```sh
  git clone https://github.com/yourusername/hexaforge.git
  cd {project}
  ```

2. **Build the Docker image using Jib**:
  ```sh
  cd {project}
  ./gradlew jibDockerBuild
  ```

## Running the Project with Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. Follow these steps to run the project:

1. **Navigate to the project directory**:
  ```sh
  cd {project}
  docker-compose up
  ```

2. **Access the application**:
  Open your web browser and go to `http://localhost:8080` (you can change the port in the `docker-compose.yml` file).

## Stopping the Application
  To stop the application, run:
  ```sh
  docker-compose down
  ```

## Features

1. **Swagger**:
  [springdoc-openapi](https://springdoc.org/#Introduction) is used to generate OpenAPI documentation for your application and can be found at `http://localhost:8080/swagger-ui/index.html`.
