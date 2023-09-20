# Pull official base Python Docker image
FROM python:3.11.3

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
RUN pip install uwsgi

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN chmod +x /code/sunbeihai/worker_entrypoint.sh

CMD ["chmod", "+x", "./wait-for-it.sh"]