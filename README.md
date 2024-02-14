# Flask interview test

## API endpoints
### Change balance based on temperature
/update_balance

available methods: POST

arguments:
```
user_id: the id of the user
city: the name of the city
```

### Get users
/manage_users

GET request: gets all users

### Add users
/manage_users

POST request: adds new user

arguments: username, balance

### Update users
/manage_users

PUT request: updates existing user

argmuments: user_id, balance

### Delete users
/manage_users

DELETE request: deletes user

arguments: user_id
