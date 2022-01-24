# Docker in practice

## Database
We've used Postgres as our database. We used an `sql` script to perform the first-time database related initializations such as creating database and user. Take a look at the `postgres_init.sql` to customize per your need. 

### Database Migrations
It's very important to be able to manage database tables migrations and schema updates as our service grows or tables schema changes over time. 
We use SQLAlchemy `alembic` to manage database migrations. To read more https://alembic.sqlalchemy.org/. 

Follow the below steps to enable `alembic` migration for your service. 
There are different ways to use `alembic` library in your service. I've described two different methods. 

1. Go into a directory and create a python virtual environment, and activate it. 
```bash
cd /path/to/a/dir
python3 -m venv venv
source venv/bin/activate
```

2. Add `alembic` to `requirements.txt` file and install packages:
```bash
pip install -r config/requirements.txt
```
Or install it directly in your environment: 
```bash
pip install alembic
```

3. Go into the `tutorial04` dir, and update the `PYTHONPATH` environment variable: 
```bash
export PYTHONPATH=$PYTHONPATH:$PWD:$PWD/apps
```

4. Go into the `tutorial04/apps` directory, and initialize alembic, by which `alembic.ini` file and `migrations` directory are created.
```bash
alembic init migrations
```

**Important**: Once you did the above 4 steps, there are two options for you to enable alembic. 
#### a. Using Virtual Environment
*Please make sure that your database is up and accessible from localhost*. 

5. From the `tutorial04/apps` directory, run the following command to generate the first migration version. It will automatically detect changes and create a revision file. 
```bash
alembic revision  --autogenerate -m "create initial tables"
```
You need to run the above command every time your tables schema changes. 

6. Finnaly, apply the changes: 
```bash
alembic upgrade head
``` 
This command will reflect the new changes into database table. 
You need to run this command every time you have new revision files. 


#### b. Using Docker Container
*Please make sure that your service is up and running*

5. First build the image and make sure `auth` service is running, then try attaching to the container. 
```bash
cd tutorial04
docker-compose build auth
docker-compose exec auth bash
```

Once iside the container, go into the `apps` directory and run the below command: 
```bash
cd apps
alembic revision --autogenerate -m "create initial tables"
```
You need to run the above command every time your tables schema change. 

6. Finnaly, apply the changes: 
```bash
alembic upgrade head
``` 
This command will reflect the new changes into database table. 
You need to run this command every time you have new revision files. 


## docker-entrypoint
In order to run a set of commands for your service to start up we can use a `docker-entrypoint.sh` file. For example, we want to do database migrations before running the service to make sure database schema are up to date. 
```bash
...
alembic upgrade head
...
```


## Caching
We used `Redis` in-memory caching app to cache objects from our services. 


## Environments
You often need to have different images for different test, production, or stage environments. Update the `TAG` value in the `.env` file for different situations. 

You can also use shell terminal ENV variables to overwrite the variables inside that file. For example `export TAG=local` will overwrite the TAG in the .env file when used by docker-compose.
```bash
export TAG=local
```


## Service Log
```bash
docker-compose logs -f <service_name>
e.g,
docker-compose logs -f auth
docker-compose logs -f webserver
```

## Multiple Dockerfiles
You can have as many Dockerfiles as you want, with just making files with ``.Dockerfile`` postfix. For example: 
* ``auth.Dockerfile`` for ``auth`` service
* ``nginx.Dockerfile`` for ``nginx`` service

## Docker ignore
Similar to ``.gitignore`` file which tells git to ignore files, we can use ``.dockerignore`` file to instruct Docker to ignore files. 

## Nginx Rate Limiting
Rate limiting can be used to prevent DDoS attacks, or prevent upstream servers from being overwhelmed by too many requests at the same time.

For example, the below config in nginx informs the web server to allow only one request per second from a given ip. 
```bash
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
```

* NGINX actually tracks requests at millisecond granularity
* What if we get 2 requests within 100ms of each other? 
  * For the second request NGINX returns status code 503 to the client. For requests that arrive at the full bucket, NGINX will respond with the 503 Service Unavailable error. 

### Buffering excessive requests
We can buffer any excess requests and service them in a timely manner. This is where we use the burst parameter to limit_req, as in this updated configuration:
```bash
    limit_req zone=mylimit burst=20;
```

The burst parameter defines how many requests a client can make in excess of the rate specified by the zone (with our sample mylimit zone, the rate limit is 10 requests per second, or 1 every 100ms). A request that arrives sooner than 100ms after the previous one is put in a queue, and here we are setting the queue size to 20.

You can read more about [nginx rate limit](https://www.nginx.com/blog/rate-limiting-nginx/).