FROM python:3.9-alpine

WORKDIR /app

RUN apk --no-cache add yarn npm
RUN yarn global add cdk8s-cli && yarn cache clean
RUN pip install pipenv

# Install dependencies
COPY . .
RUN pipenv lock --requirements > requirements.txt
RUN pip install --target=/app -r requirements.txt

CMD ["/app/main.py"]
ENTRYPOINT ["python"]