from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from src.utils.log import logger
from fastapi import APIRouter
from fastapi import Request

router = APIRouter()


@router.get("/docs", include_in_schema=False)
def swagger_ui(request: Request):
    """
    Overriding the default FastAPI /docs endpoint to provide a custom Swagger UI
    """
    logger.info(
        msg="-",
        extra={
            "status": 200,
            "method": request.method,
            "request_path": request.url.path})
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Parosly - Docs",
                               swagger_favicon_url="images/favicon.ico")


@router.get("/redoc", include_in_schema=False)
def redoc_ui(request: Request):
    """
    Overriding the default FastAPI /redoc endpoint to provide a custom ReDoc
    """
    logger.info(
        msg="-",
        extra={
            "status": 200,
            "method": request.method,
            "request_path": request.url.path})
    return get_redoc_html(openapi_url="/openapi.json", title="Parosly - Docs",
                          redoc_favicon_url="images/favicon.ico")
