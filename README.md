<h1 align="center">Gate-Keeper</h1>

Provide a username and password login to protect Nginx endpoints


## Requirements

- Python 3.8+
- Nginx
- Docker

## Installation
Build and start the container

    $ docker compose up -d --build

## Configuration

1. In Nginx server block where you want to password protect, add the following:

```
# Handle login and session management through the auth app
location ~ ^/authenticator-gate-keeper(.*)$ {
    proxy_pass http://localhost:2238$1$is_args$args;
    proxy_set_header Host $host;
    proxy_set_header X-Original-URI $request_uri;
}
```
2. Add the following to each location block that should be password protected:
```
auth_request /authenticator-gate-keeper/validate; # Validate authentication
error_page 401 = /authenticator-gate-keeper/login; # Redirect unauthorized requests to the login page
```

#### Nginx config example:
```
server {
    server_name example.org;

    # Handle login and session management through the auth app
    location ~ ^/authenticator-gate-keeper(.*)$ {
        proxy_pass http://localhost:2238$1$is_args$args;
        proxy_set_header Host $host;
        proxy_set_header X-Original-URI $request_uri;
    }
    location / {
        proxy_set_header XForwardedFor $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:8080;
        proxy_intercept_errors on;
        auth_request /authenticator-gate-keeper/validate; # Validate authentication
        error_page 401 = /authenticator-gate-keeper/login; # Redirect unauthorized requests to the login page
    }
    listen 80;
}    
```

Note: In the docker-compose.yml the value of AUTHENTICATOR_PREFIX should be the same as the one used in Nginx `authenticator-gate-keeper`


## Create users
You can generate new users using the Python script register-user.py:

    $ docker exec -it gatekeeper-auth-app-1 bash
    $ python register-user.py

It will ask to enter a username and a password then will store it encrypted in the file users.json.

## License
This work is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

The license allows you to use and modify the work for personal and commercial purposes, but if you distribute the work you must provide users with a means to access the source code for the version you are distributing. Read more about the [GPLv3 at TL;DR Legal](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
