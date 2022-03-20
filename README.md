# Installation:

> Prerequisites:
>
> - [Docker](https://docker.com)

Simply run the following command and the service should be running at this url: http://localhost:8000/
``` bash
docker-compose up
```

> Note:  
> The pokemonTypes are generated automatically by a django command `populate_pokemon_types` 
> when the docker start. This command takes the data from https://pokeapi.co/api/v2/type
> and populate pokemonTypes with it

From there you can either use a tool like Postman or use the Django Rest Framework web ui.

Also, to simplify the creation of an account, I added an endpoint `POST http://localhost:8000/api/signup/`  
Params are :
- `email`
- `password`

### List of endpoint:
- `POST http://localhost:8000/api/signup/`  
- `POST http://localhost:8000/api/login/`  
- `POST http://localhost:8000/api/token/refresh/`  
- `POST http://localhost:8000/api/token/verify/`  
- `POST http://localhost:8000/api/group/<type>/add/`  
- `POST http://localhost:8000/api/group/<type>/remove/`  
- `GET http://localhost:8000/api/me/`  
- `GET http://localhost:8000/api/pokemon/`  
- `GET http://localhost:8000/api/pokemon/<name|id>/`  

### Django admin:

if you wish to access the admin at this url `http://localhost:8000/`
You will need to create a superuser first:
``` bash
# bash in the app container
docker-compose exec app bash

# run this command to create a superuser
./manage.py createsuperuser
```

### Test

You can run the test directly in the docker:
```bash
docker-compose exec app bash

# in the container
./manage.py test
```

Or you can use tox to perform different tests (flake8, isort, black and app test).  
First install tox:

`pip install tox`

then in the project folder run: 

`tox`

You should see the following:

``` bash
flake8: commands succeeded
black: commands succeeded
isort: commands succeeded
test: commands succeeded
congratulations :)

```

