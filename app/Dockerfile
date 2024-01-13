
FROM python:3.9-slim

# Working directory in the container
WORKDIR /usr/src/app

# Install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container at /usr/src/app
COPY Pipfile Pipfile.lock ./

# Install any needed packages specified in Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of your application's code into the container at /usr/src/app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app using pipenv to ensure the right Python environment
CMD ["pipenv", "run", "flask", "run"]
