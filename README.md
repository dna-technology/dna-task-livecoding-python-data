## Setting up the app

Before running Docker container copy `docker-compose.override.dist.yml` to `docker-compose.override.yml` and replace default values
so you are sure everything will work properly.

Then to start the application run following command in your terminal

```sh
docker-compose up
```

Then you should be able to run tests with simple command
```sh
docker-compose exec app pytest
```
