# hades
backend for inventory application 


after create postgresql database on 127.0.0.1:5432
python manage.py migrate
run python manage.py runserver


# api
endpoints:

# POST
http://127.0.0.1:8000/users/oauth
```
{
    'id_token': <id_token>
    'provider': google
}

```
```
Response
{
  "email": "john@gmail.com",
  "nickname": "John",
  "access_token": access_token,
  "refresh_token": refresh_token
}

```
# To next api endpoints we need to send access_token

#GET
http://127.0.0.1:8000/users/me

#POST
127.0.0.1:8000/projects
{
    'name': '<project name>'
    'company_name': '<company_name>'
}

# GET
127.0.0.1:8000/projects
{
    list of user ids
}
127.0.0.1:8000/projects/<project_id>
{
    project detail
}
