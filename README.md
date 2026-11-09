# Campus Lost & Found API

A backend API where students report lost and found items on campus, claim items, and comment on them. Built with Django and Django REST Framework.

## Features

- Models: Item, Claim, Comment (foreign keys, plus a many-to-many `watchers` field on Item)
- Status choices on Item (lost, found, claimed, returned) and Claim (pending, approved, rejected)
- Django admin with search, filters and inline claims and comments
- REST API with full CRUD for items, claims and comments
- Pagination (5 per page) and input validation
- Tests for the API, including bad-input cases

## Run it locally

```
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py seed
pipenv run python manage.py createsuperuser
pipenv run python manage.py runserver
```

- API: http://127.0.0.1:8000/api/items/
- Admin: http://127.0.0.1:8000/admin/

## Endpoints

| Path | Description |
| --- | --- |
| `/api/items/` | List and create items |
| `/api/items/<id>/` | Retrieve, update, delete an item |
| `/api/claims/` | List and create claims |
| `/api/comments/` | List and create comments |

## Run the tests

```
pipenv run python manage.py test
```