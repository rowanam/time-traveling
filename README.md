# Time Traveling

An app to visualize your travels

## Google Maps API

### Steps to set up

[Quickstart documentation](https://developers.google.com/maps/gmp-get-started#quickstart)

- Create new project on Google Maps Platform and enable billing
- Enable APIs and get API key

## Technologies Used

- [Django (v3.2)](https://docs.djangoproject.com/en/3.2/)
- Leaflet
- [Bootstrap (v5.3)](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Cloudinary](https://cloudinary.com/) - media storage
- [ElephantSQL](https://www.elephantsql.com/) - external database

### Libraries

Database connection:

- dj_database_url
- psycopg2

Authentication:

- [django-allauth (0.44.0)](https://docs.allauth.org/en/latest/)

Map interaction:

- [leaflet-geosearch](https://github.com/smeijer/leaflet-geosearch)

Deployment server:

- gunicorn

## Attributions

- Logo and favicon - [Logo.com](https://logo.com/)
- Main background - [Image by GarryKillian](https://www.freepik.com/free-vector/terrain-big-data-visualization_7941096.htm#query=dark%20map&position=0&from_view=search&track=ais&uuid=7850fb46-cc4c-401c-bb49-be112d860467) on Freepik