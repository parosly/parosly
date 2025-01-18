from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI


def openapi(app: FastAPI):
    """
    This function customizes the OpenAPI definition
    and adds a logo for the ReDoc API page. NOTE: this
    does not include a definition of the routes
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Parosly",
        summary="Extended HTTP API service for Prometheus",
        description="This project enhances the native Prometheus HTTP API by "
                    "providing additional features and addressing its limitations. "
                    "Running as a sidecar alongside the Prometheus server enables "
                    "users to extend the capabilities of the API.",
        version="0.2.0",
        contact={
            "name": "Hayk Davtyan",
            "url": "https://hayk96.github.io",
            "email": "hayk@parosly.io",
        },
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
            "url": "https://raw.githubusercontent.com/parosly/parosly/main/LICENSE"
        },
        routes=app.routes,
        servers=[{"url": 'https://example.com'}]
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/parosly/parosly/refs/heads/main/ui/assets/images/logo-parosly.svg",
        "href": "https://docs.parosly.io",
        "altText": "Parosly"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema
