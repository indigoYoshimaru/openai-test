# Use the Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR .

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml .
COPY rda/.env .
COPY . .

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install

# Permit main file if you use sudo
RUN chmod +x ./rda/__main__.py

# Set the entrypoint command to run the application
CMD ["poetry", "run", "rda", "run-app"]