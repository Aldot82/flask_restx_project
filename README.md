# passnfly_test
Pasnnfly technical test

## build
docker-compose build

## up
docker-compose up

## run migrations 
docker exec -it container_name flask db init  
docker exec -it container_name flask db migrate -m "whatever"  
docker exec -it container_name flask db upgrade
  
## run tests
docker exec -it container_name coverage run -m pytest tests
  
## coverage report
docker exec -it container_name coverage report
