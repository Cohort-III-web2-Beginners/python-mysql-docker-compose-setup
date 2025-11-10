

### login mysql in your container
```docker
docker exec -it <name_of_db_container> mysql -u <user_db> -p

e.g.
docker exec -it todoapp_db mysql -u root -p
```
