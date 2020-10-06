# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 13800 available to the world outside this container
EXPOSE 13800

# Define environmental variable
ENV ADDRESS=not_set
ENV VIEW=not_set

# Run phase1.py when the container launches
CMD ["python", "app.py"]
