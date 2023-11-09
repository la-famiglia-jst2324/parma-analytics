# parma-prod-db ORM

This directory contains the ORM for the production database.

## RAW SQL Queries vs. ORM

We use the ORM for most of our queries. However, for some queries, the ORM is not expressive enough. In these cases, we might use raw SQL queries. We try to limit the use of dynamically created raw SQL queries to a minimum as they cannot be linted properly.

## submodules

While this package includes querying logic for all the tables in the database, we have separated the ORM models into the `models` submodule.
This is to make the code more readable and maintainable.

Checkout `./models/README.md` for more the ER diagram and more information about the models.
