# fastapi-demo-aws

watch the demo on [youtube](https://youtu.be/eYcTuRIWYd0)


## getting started

> __note__: this repository assumes your local dev environment is unix-based (macOS, WSL2, linux) with python3, git and docker desktop configured

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

## local database migrations

> __note__: the application must be up and running before using the following commands.  you will always want to create your database migrations locally so that it can be checked into source code and versioned with deployments.

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

## aws ssh setup

> __note__: this section assumes you have the following cloud infrastructure provisioned:
>   * elastic container registry
>   * application load balancer
>   * application load balancer security group
>   * application load balancer target group
>   * postgresql relational database instance
>   * relational database security group
>   * elastic container task definition
>   * elastic container cluster
>   * elastic container service within cluster
>   * elastic container cluster ssh key

1. locate your `.pem` ssh key file that was downloaded when creating the ecs cluster

2. open the file with a basic text editor (vim, textEdit, notepad++, etc.)

3. copy the contents of the file

4. in your terminal, navigate to the hidden ssh directory and create a new file with the same name as your ssh key file:

    ```sh
    cd ~/.ssh # navigate to ssh directory
    vim your_key_name.pem
    ```

5. once you're in the vim editor, hit `i` on your keyboard to begin typing, you'll see `INSERT` in the bottom left corner of your editor.  paste in the contents from the downloaded ssh key file.

6. to save and quit, hit `esc`, followed by `:wq`.  The colon and wq should appear in the bottom left corner of your editor where you saw the `INSERT` statement from earlier.  Finally, hit the `enter` and you should return to your terminal in the `.ssh` directory.

7. change the permissions on the file you just created to enable the file's usage when running ssh commands:

    ```sh
    chmod 400 your_key_name.pem
    ```

8. finally, obtain a list of the ec2 instances (servers) that are available for your container to run on.  if you followed my youtube tutorial, there should be 4 instances.  clicking on each instance should present a `connect` button in the aws console.  once you've clicked the `connect` button, navigate to the `SSH client` tab to see the command for `connect[ing] to your instance using its Public DNS`.  We'll modify this command so that we can call it outside of `.ssh` directory, like if we wanted to use it in a script:

    ```sh
    ssh -i "~/.ssh/your_key_name.pem" ec2-user@ec2-35-85-180-45.us-west-2.compute.amazonaws.com
    ```

9. run the modified ssh command for each of your instances.  the first time you run the command, you will be prompted to accept the connection.  type `yes` and hit enter.  to exit the ssh connection in your ec2 instance use `ctrl` and `c` at the same time on your keyboard.


## aws deployment

> __note__: this section assumes you have the AWS CLI v2 installed and configured and the following cloud infrastructure provisioned:
>   * elastic container registry
>   * application load balancer
>   * application load balancer security group
>   * application load balancer target group
>   * postgresql relational database instance
>   * relational database security group
>   * elastic container task definition
>   * elastic container cluster
>   * elastic container service within cluster
>   * elastic container cluster ssh key
>
> __if you have not deployed your container image to the elastic container registry, comment out line 23 of the deploy.sh script since you likely do not have an ecs service__


1. visit `project/alembic.ini` and update line 53 w/ your production database URI (change this back after deploying so you don't commit your prod password to github):

    ```ini
    sqlalchemy.url = postgresql+asyncpg://db_username:db_password@rds_endpoint:5432/inital_db_name
    ```

2. visit `deploy.sh` and update the variables to match your credentials:

    ```sh
    # variables
    aws_region="us-east-1"
    aws_account_id="2893821284"
    aws_ecr_name="api"
    aws_cluster_name="api-cluster"
    aws_service_name="api-sv"
    ```

3. execute the script to build new images and update the ecs service:

    ```sh
    bash deploy.sh
    ```

4. if you have database migrations to apply, you'll need to ssh into one of your ec2 instances:

    ```sh
    ssh -i "~/.ssh/your_key_name.pem" ec2-user@ec2-35-85-180-45.us-west-2.compute.amazonaws.com
    ```

5. then list the running containers on the server:

    ```sh
    docker ps
    ```

6. if you don't see your fastapi container running, no worries.  just quit the ssh session and try with one of the other instances you provisioned.  you can also go into the aws console, find the running task in ecs, and find the linked ec2 instance it's running on.

7. once you see your container running on the server, copy the container id and bash into the container:

    ```sh
    docker exec -it your_container_id bash
    ```

8. finally, run the migration command:

    ```sh
    alembic upgrade head
    ```