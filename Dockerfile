# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create a directory for the app and set it as the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application source code
COPY . .

# Stage 2: Runtime stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Ensure the runtime uses the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Run the application
CMD ["python", "app.py"]

