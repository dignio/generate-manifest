FROM python:3.9-slim AS builder
ADD . /app
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Install dependencies
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install --target=/app -r requirements.txt

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10

COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

CMD ["/app/main.py"]