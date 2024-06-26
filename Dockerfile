FROM python:3.11.3

# Set a working directory inside the container
WORKDIR /usr/src

# Copy only the necessary files for installing dependencies
# This layer is cached and speeds up builds if these files have not changed
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Disable virtual environments created by Poetry
# This is necessary for Docker since we want the packages to be globally accessible in the container
RUN poetry config virtualenvs.create false

# Install project dependencies using Poetry
RUN poetry install --no-dev
# Use --no-dev if you don't need development dependencies

# Copy the rest of your application's code to the container
COPY src /usr/src

CMD python /usr/src/main.py
