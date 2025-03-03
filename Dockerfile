
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code/

# Copy the project files
COPY . /code/

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
