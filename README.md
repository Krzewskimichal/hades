# hades
backend for inventory application 


after create postgresql database on 127.0.0.1:5432
python manage.py migrate
run python manage.py runserver

For docker-compose(docker-compose up)

# api
endpoints:

### POST  - get refresh and access token
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
### POST - get access token 
http://127.0.0.1:8000/users/api/token/refresh
{
    "refresh": <refresh_token>
}

### GET
http://127.0.0.1:8000/users/me



### POST - create project
127.0.0.1:8000/projects
{
    'name': '<project name>'
    'company_name': '<company_name>'
}
### GET - get all projects assigment to user or project info by id
127.0.0.1:8000/projects
127.0.0.1:8000/projects/<project_id>
### PATCH - update project
127.0.0.1:8000/projects/<project_id>
{
    'name': '<new project name>'
}
### DELETE - delete project
127.0.0.1:8000/projects/<project_id>

# Loalization/inventory_item_status/inventory_type_status
the same endpoints for all of them

localization -> 127.0.0.1:8000/localization/<project_id>
inventory_item_type -> 127.0.0.1:8000/inventory-type/<project_id>
inventory_item_status -> 127.0.0.1:8000/inventory-status/<project_id>

## Example for localization
### POST - create localizations for project
127.0.0.1:8000/localization
{
    'project': '<project_id>'
    'place': '<place_name>'
}
### GET - get all localization assigment to project or localization info by id
127.0.0.1:8000/localization/<project_id>
127.0.0.1:8000/localization/<project_id>/<localization_id>
### PATCH - update localization
127.0.0.1:8000/projects/<project_id>
{
    'place': '<new place name>'
}
### DELETE - delete localization
127.0.0.1:8000/localization/<project_id>/<localization_id>


# Inventory item
### GET - get all item assigment to project or item info by id
127.0.0.1:8000/inventory-item/<project_id>
127.0.0.1:8000/inventory-item/<project_id>/<inventory-item_id>

### POST - create item
127.0.0.1:8000/inventory-item/<project_id>
{
    "image": null,
    "name": "laptop", - **required**
    "brand": "Lenovo",
    "model": "G70",
    "serial_number": "123098653",
    "qr_key": "920b3694-b20e-4282-93d1-50026affd76b",
    "custom_field": null, - **JSON addictional field**
    "inventory_type": null, - **type id**
    "localization": null, - **loc id**
    "status": null, - **status id**
    "employee": null, - **user id**
    "project": 17 - **project id**
}

### PATCH - update item
127.0.0.1:8000/inventory-item/<project_id>/<item_id>
{
    "name": "laptop",
    "brand": "Lenovo",
    "model": "G70",
    "qr_key": "920b3694-b20e-4282-93d1-50026affd76b",
    "custom_field": null,

}

### DELETE - delete item
127.0.0.1:8000/inventory-item/<project_id>/<item_id>

# Add user to project

### POST
127.0.0.1:8000/project_users/<project_id>
{
    "email": "<user_email>",
    "role": "OW"/"AD"/"WA"/"EM"

}
roles:
'OW': 'Owner'
'AD': 'Admin'
'WA': 'Warehouseman'
'EM': 'Employee'

### DELETE
127.0.0.1:8000/project_users/<project_id>?id=<user_id>
