# Description
 
Autocompany online shop

# Requirements

- Python 3.11.2
- Docker 18+, docker-compose 1.13.0

### Setting up development environment

Append the following line to `/etc/hosts`:
```
127.0.0.1 autocompany-postgres autocompany-postgres-test
```
#### Creating virtual env through pyenv

Run the following to install the correct Python version, and setup a virtual env that uses that version.

```
PYTHON_VER=3.11.2
pyenv install $PYTHON_VER
pyenv virtualenv $PYTHON_VER autocompany
```

Then it is time to install our dependencies.

```sh
  pip install -r requirements-dev.txt
```

Env is now setup! 


# Linting

All linting is run as a git commit hook.

### Git hooks

Git hooks need to be set up manually.
1. Remove the existing files in the `.git/hooks` directory.  Note this is NOT the same directory as `.githooks`.
   ```shell script
   rm .git/hooks/*
   ``` 
2. Copy the files found in `.githooks/hooks_to_copy` to `.git/hooks`. 
   ```shell script
   ln -s ../../.githooks/hooks_to_copy/pre-commit .git/hooks/pre-commit
   ``` 

### How to run linters manually

If your IDE integrates with `ruff`, and `pylint` please set it up.  To run the linters manually, these commands can be used:
```sh
    bandit -c pyproject.toml -r .
    black autocompany/
    isort  autocompany/
    pylint autocompany/
    ruff autocompany/
```

#### Black

Additionally `black` is used for automatic code formatting. It runs as a commit hook, but we recommend
to set it up for your IDE:

https://black.readthedocs.io/en/stable/integrations/editors.html

The config for `black` can be found in the pyproject.tml file in root.


# How to

### How to run the app using Docker and Postgresql


1. First of all fire docker containers!
```sh
docker-compose up -d
```
2. Run migrations to populate the DB. After the MVP we can automate this :) And create admin user.
```sh
 docker-compose run autocompany-web python manage.py migrate
 docker-compose run autocompany-web python manage.py createsuperuser
```
3. All good!  You can access the Swagger UI [here](http://localhost/swagger/) and Admin page [here](http://localhost/admin/)

4. Optional: If you like to add sample products, run this command.
```sh
docker-compose run autocompany-web python manage.py seed_products
```

### Notes

-  Authentication: Here I'm using JWT for the authentication. Users will be able to see the products list and individual
products without authenticating. But for the rest of the endpoints they need to authenticate.
And to create, update or delete a product you need to be superuser.

Makesure to include 'Bearer' prefix before the token when you try with Swagger UI.
Ex: 
```
# Get a token for given user. Here I'm using superadmin credentials but if you want you can register new user.

# Optional: Create new user
curl -X 'POST' \
  'http://localhost:8001/api/v1/user/register/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user",
  "password": "user"
}'

curl -X 'POST' \
  'http://localhost:8001/api/auth/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "password": "admin"
}'

# Create new product. Yeah only superadmin can create anyway :) 
curl -X 'POST' \
  'http://localhost:8001/api/v1/products/' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer xxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_code": "P-0005",
  "name": "Cool product",
  "description": "Cool product description",
  "price": "10",
  "sku": "sku",
  "quantity": 50
}'

# Submit the order
curl -X 'POST' \
  'http://localhost:8001/api/v1/orders/' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer xxx' \
  -H 'Content-Type: application/json' \
  -d '{
  "delivery_date": "2023-10-03T18:51:50.956Z"
}'
```

### Future enhancements 

- Include product category and product image which may store in SWS S3.
