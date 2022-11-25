# hades
backend for inventory application 


after create postgresql database on 127.0.0.1:5432
python manage.py migrate
run python manage.py runserver


# api
endpoints:

# POST  - get refresh and access token
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
# POST - get access token 
http://127.0.0.1:8000/users/api/token/refresh
{
    "refresh": <refresh_token>
}

#GET
http://127.0.0.1:8000/users/me



#POST - create project
127.0.0.1:8000/projects
{
    'name': '<project name>'
    'company_name': '<company_name>'
}
# GET - get all projects assigment to user or project info by id
127.0.0.1:8000/projects
127.0.0.1:8000/projects/<project_id>
# PATCH - update project
127.0.0.1:8000/projects/<project_id>
{
    'name': '<new project name>'
}
# DELETE - delete project
127.0.0.1:8000/projects/<project_id>


#POST - create localizations for project
127.0.0.1:8000/localization
{
    'project': '<project_id>'
    'place': '<place_name>'
}
# GET - get all localization assigment to project or localization info by id
127.0.0.1:8000/localization/
127.0.0.1:8000/localization/<project_id>/<localization_id>
# PATCH - update localization
127.0.0.1:8000/projects/<project_id>
{
    'place': '<new place name>'
}
# DELETE - delete localization
127.0.0.1:8000/localization/<project_id>/<localization_id>

