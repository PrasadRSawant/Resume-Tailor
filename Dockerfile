# Stage 1: Build Stage
FROM python:3.10-slim-buster AS builder

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime Stage
FROM python:3.10-slim-buster AS runtime

# Set the working directory in the container
WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code into the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --port 8000 specifies the port
# The app:app refers to the 'app' instance in the 'app.main' module (assuming app/main.py and an 'app' instance)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
