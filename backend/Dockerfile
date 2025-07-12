# Pull official latest Python Docker image (Pulished with version 3.11.0)
FROM --platform=linux/amd64 python:latest

# Set the working directory
WORKDIR /usr/backend

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the server port
EXPOSE 8000

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-openbsd gcc \
  && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy scripts first
COPY ./scripts /scripts
RUN chmod +x /scripts/entrypoint_project.sh /scripts/entrypoint_alembic.sh /scripts/entrypoint_alembic_revision.sh

# Copy all files
COPY . .
ENV PYTHONPATH=/usr/backend
RUN sed -i 's/\r$//' /usr/backend/entrypoint.sh
RUN chmod +x /usr/backend/entrypoint.sh

# Execute entrypoint.sh
ENTRYPOINT ["/usr/backend/entrypoint.sh" ]

# Start up the backend server
CMD ["uvicorn", "src.main:backend_app", "--reload", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
