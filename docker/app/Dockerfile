# Use an official Python runtime as a base image
FROM python:3.10-slim



# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

