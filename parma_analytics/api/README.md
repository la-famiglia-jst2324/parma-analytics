# Parma Analytics API

FastAPI subpackage for the Parma Analytics API.

The openapi docs are available at the `/docs` and `/redoc` routes.

## API Design Principles

- RESTful
- CRUD:
  - Create > `HTTP POST`
  - Read > `HTTP GET`
  - Update > `HTTP PUT`
  - Delete > `HTTP DELETE`

API Models and endpoints (routes) are separated into submodules the submodules `models` and `routes` respectively.

Checkout the respective READMEs for more information.
