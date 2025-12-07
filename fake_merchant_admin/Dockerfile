# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Flask
RUN pip install Flask

# Expose internal port
EXPOSE 5900

# Default run command
CMD ["python", "app.py"]
