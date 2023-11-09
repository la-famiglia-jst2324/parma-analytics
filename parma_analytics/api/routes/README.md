# FastAPI routes

This subpackage contains all the routes of the API.

Different domains are separated into different modules.

## Route Design Principles

- **Consistency**: All routes should follow a consistent naming convention and structure.
- **Clarity**: All routes should be clear and unambiguous.
- **Simplicity**: All routes should be simple and easy to understand.
- **Type annotations**: All routes should be type annotated both in input and output. This allowed fastapi to automatically generate the OpenAPI schema and documentation.
- **appropriate HTTP status codes**: All routes should return the appropriate HTTP status codes.
