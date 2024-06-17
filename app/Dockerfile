# Use the official Python 3.9 Alpine image from the Docker Hub
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev curl

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and Werkzeug with compatible versions
RUN pip install flask==2.1.1 werkzeug==2.0.3

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]