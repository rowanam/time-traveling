# Time Traveling

An app to visualize your travels

## Google Maps API

### Steps to set up

[Quickstart documentation](https://developers.google.com/maps/gmp-get-started#quickstart)

- Create new project on Google Maps Platform and enable billing
- Enable APIs and get API key

## Technologies Used

- [Django (v3.2)](https://docs.djangoproject.com/en/3.2/)
- Google Maps API
- [Bootstrap (v5.3)](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Cloudinary](https://cloudinary.com/) - media storage
- [ElephantSQL](https://www.elephantsql.com/) - external database

### Libraries

Database connection:

- dj_database_url
- psycopg2

Authentication:

- [django-allauth (0.44.0)](https://docs.allauth.org/en/latest/)

Deployment server:

- gunicorn