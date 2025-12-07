FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Tor only
RUN apt update && apt install -y tor curl

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose app port
EXPOSE 5000

# Default command (overridden by docker-compose)
CMD ["python", "amex_gateway.py"]
