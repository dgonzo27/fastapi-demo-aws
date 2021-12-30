# fastapi-demo-aws

watch the demo on [youtube](https://youtu.be/f9BwGhUnK6s)


## getting started

1. build the docker containers:

    ```sh
    docker compose build
    ```

2. run the containers in detached mode:

    ```sh
    docker compose up -d
    ```

3. apply database migrations:

    ```sh
    docker compose exec api alembic upgrade head
    ```

4. visit `http://localhost:8000/docs` to create and get movies

5. stop the containers:

    ```sh
    docker compose down
    ```

## database migrations

> __note__: the application must be up and running before using the following commands

1. create a new migration:

    ```sh
    docker compose exec api alembic revision --autogenerate -m "your comment here"
    ```

2. apply migrations:

    ```sh
    docker compose exec api alembic upgrade head
    ```

3. revert a migration:

    ```sh
    docker compose exec api alembic downgrade -1
    ```

## aws deployment

1. build and push a new image and update the ecs service:

    ```sh
    bash deploy.sh
    ```