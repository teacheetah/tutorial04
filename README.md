# Docker in practice

## Database
We've used Postgres database. 

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