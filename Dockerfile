FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
# RUN npm i -g cdk8s-cli
RUN pip install pipenv

# Install dependencies
COPY . .

RUN pipenv install --system --deploy

ENTRYPOINT ["/app/main.py"]
