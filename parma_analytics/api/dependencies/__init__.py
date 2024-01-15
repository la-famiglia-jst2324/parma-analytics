"""This package contains dependency functions used across the routes.

These dependencies are designed to provide reusable utility functions, such as
authentication and authorization checks, that can be injected into FastAPI route
handlers. By centralizing these dependencies, the application's code remains
clean, modular, and easy to maintain.

Each module in this package is tailored to specific sets of functionalities. For
example, `sourcing_auth.py` handles authentication for sourcing modules, thereby
organizing the dependencies in a clear and logical manner.
"""
