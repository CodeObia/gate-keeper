# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask requests flask-login gunicorn python-dotenv

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["sh", "-c", "python generate-app-secret-key.py && gunicorn -w 1 -b 0.0.0.0:5000 app:app"]