from sys import modules

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator

from .log import logger


def metrics(app: FastAPI):
    """
    This function exposes Prometheus
    metrics for Parosly service
    """
    metrics_path = "/api-metrics"
    try:
        instrumentator = PrometheusFastApiInstrumentator(
            should_group_status_codes=False, excluded_handlers=["/{path:path}", "/.*metrics"]
        )
        instrumentator.instrument(app)
        instrumentator.expose(app, endpoint=metrics_path, tags=["metrics"])
    except BaseException as e:
        logger.error(f"{modules[__name__], e}")
    else:
        logger.info(f"Successfully started metrics endpoint at {metrics_path} path")
