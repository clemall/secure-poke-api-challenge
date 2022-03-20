# Installation:

> Prerequisites:
>
> - [Docker](https://docker.com)

Simply run the following command and the service should run at this url: http://localhost:8000/
``` bash
docker-compose up
```

> Note:  
> The pokemonTypes are generated automatically by the django command `populate_pokemon_types` 
> when the docker starts. This command takes the data from https://pokeapi.co/api/v2/type
> and populate pokemonTypes with it.

From there you can either use an API testing tool such as Postman or the Django Rest Framework Web UI.

To simplify the creation of an account, I added the endpoint `POST http://localhost:8000/api/signup/`.  
The params are as follows:
- `email`
- `password`

### List of endpoints:
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

if you wish to access the admin at the url `http://localhost:8000/`, 
you first need to create a superuser:
``` bash
# bash in the app container
docker-compose exec app bash

# run this command to create a superuser
./manage.py createsuperuser
```

### Test

You can run the test directly in the docker container:
```bash
docker-compose exec app bash

# in the container
./manage.py test
```

Or you can use Tox to perform different tests (flake8, isort, black and app test).  
First install Tox:

`pip install tox`

then run the following command in the project folder: 

`tox`

You should see the following:

``` bash
flake8: commands succeeded
black: commands succeeded
isort: commands succeeded
test: commands succeeded
congratulations :)

```


### Possible improvements

- Make a daily task (with Celery for instance) that will run the populate_pokemon_types script.
- Add caching in the pokeapi wrapper to avoid the call to an external api.
