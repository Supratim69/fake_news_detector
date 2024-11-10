# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the app code into the working directory
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
