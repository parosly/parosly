"""Parsoly API endpoints for Prometheus configuration parts."""

from typing import Annotated, TypedDict

import yaml
from deepmerge import always_merger
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.core.prometheus import PrometheusAPIClient
from src.models.prometheus.configs._globals import GlobalConfig
from src.models.prometheus.configs.alerting import AlertingConfig
from src.models.prometheus.configs.runtime import RuntimeConfig
from src.models.prometheus.configs.scrape import ScrapeConfig
from src.utils.log import logger


class ConfigPartResponse(BaseModel):
    """Default response model for Prometheus configuration parts.

    Attributes:
        status (str): The status of the configuration update.
        message (str): A message describing the status of the configuration update.
    """

    status: str
    message: str


router = APIRouter(
    prefix="/api/v1/config",
    responses={
        500: {
            "description": "Internal Server Error",
            "model": ConfigPartResponse,
        },
    },
)


class RuleFiles(TypedDict):
    """Rules Files configuration model.

    Attributes:
        rule_files (list[str]): A list of rule files.
    """

    rule_files: list[str]


class ScrapeConfigFiles(TypedDict):
    """Scrape Config Files configuration model.

    Attributes:
        scrape_config_files (list[str]): A list of scrape config files.
    """

    scrape_config_files: list[str]


class ScrapeConfigs(TypedDict):
    """Scrape Configs model.

    Attributes:
        scrape_configs (list[ScrapeConfig]): A list of scrape config models.
    """

    scrape_configs: list[ScrapeConfig]


async def prometheus_client() -> PrometheusAPIClient:
    """API Dependency that returns a PrometheusAPIClient instance.

    Returns:
        PrometheusAPIClient: An instance of the PrometheusAPIClient class.
    """
    return PrometheusAPIClient()


async def save_config_part(
    config: dict,
    request: Request,
    prom: PrometheusAPIClient,
    *,
    sort_keys: bool,
) -> ConfigPartResponse:
    """Save a Prometheus configuration part.

    Args:
        config (dict): The updated Prometheus configuration.
        request (Request): The incoming request object.
        prom (PrometheusAPIClient): The Prometheus API client instance.
        sort_keys (bool): Whether to sort the YAML keys when writing the configuration.

    Returns:
        ConfigPartResponse: The response model for the configuration update.
    """
    data_yaml = yaml.dump(config, Dumper=yaml.SafeDumper, sort_keys=sort_keys)
    config_update_status, msg = prom.update_config(data=data_yaml)
    if config_update_status:
        status_code, sts, msg = prom.reload()
        msg = "Configuration updated successfully" if sts == "success" else msg
    else:
        status_code, sts = 500, "error"
    logger.info(
        msg=msg,
        extra={
            "status": status_code,
            "method": request.method,
            "request_path": request.url.path,
        },
    )

    return {"status": sts, "message": msg}


@router.get("/global", tags=["Global"])
async def get_global_config(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> GlobalConfig:
    """Get the global Prometheus configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return data["global"]


@router.patch("/global", tags=["Global"])
async def update_global_config(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    config: GlobalConfig,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the global Prometheus configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    data.update({"global": config.dict()})
    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.get("/runtime", tags=["Runtime"])
async def get_runtime_config(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> RuntimeConfig:
    """Get the runtime Prometheus configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return data["runtime"]


@router.patch("/runtime", tags=["Runtime"])
async def update_runtime_config(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    config: RuntimeConfig,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the runtime Prometheus configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    data.update({"runtime": config.dict()})
    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.get("/rule_files", tags=["Rule Files"])
async def get_rule_files(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> RuleFiles:
    """Get the Prometheus rule files."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return {"rule_files": data["rule_files"]}


@router.patch("/rule_files", tags=["Rule Files"])
async def update_rule_files(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    rule_files: RuleFiles,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the Prometheus rule files, with deduplication."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)

    for file in rule_files["rule_files"]:
        if file not in data["rule_files"]:
            data["rule_files"].append(file)

    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.delete("/rule_files", tags=["Rule Files"])
async def delete_rule_files(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    rule_files: RuleFiles,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> RuleFiles:
    """Get the Prometheus rule files."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    for file in rule_files["rule_files"]:
        if file in data["rule_files"]:
            data["rule_files"].remove(file)
    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.get("/scrape_configs", tags=["Scrape Configs"])
async def get_scrape_configs(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> ScrapeConfigs:
    """Get the Prometheus scrape configurations."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return {"scrape_configs": data["scrape_configs"]}


@router.patch("/scrape_configs", tags=["Scrape Configs"])
async def update_scrape_configs(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    configs: ScrapeConfigs,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the Prometheus scrape configurations."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)

    config_exists = False
    for config in configs["scrape_configs"]:
        for scrape_config in data["scrape_configs"]:
            if scrape_config["job_name"] == config["job_name"]:
                # Use deepmerge to merge the existing scrape config with the new changes
                always_merger.merge(scrape_config, config)
                config_exists = True
                break

        if not config_exists:
            data["scrape_configs"].append(config)

    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.delete("/scrape_configs", tags=["Scrape Configs"])
async def delete_scrape_config(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    job_name: str,
) -> JSONResponse:
    """Delete a Prometheus scrape configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)

    deleted = False
    for scrape_config in data["scrape_configs"]:
        if scrape_config["job_name"] == job_name:
            data["scrape_configs"].remove(scrape_config)
            deleted = True
            break

    if not deleted:
        return JSONResponse(
            content={"status": "error", "message": f"Scrape config '{job_name}' not found"},
            status_code=404,
        )

    return await save_config_part(data, request, prom, sort_keys=False)


@router.get("/scrape_config_files", tags=["Scrape Config Files"])
async def get_scrape_config_files(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> ScrapeConfigFiles:
    """Get the Prometheus scrape configurations."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return {"scrape_config_files": data["scrape_config_files"]}


@router.patch("/scrape_config_files", tags=["Scrape Config Files"])
async def update_scrape_config_files(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    scrape_config_files: ScrapeConfigFiles,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the Prometheus scrape configurations."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)

    for file in scrape_config_files["scrape_config_files"]:
        if file not in data["scrape_config_files"]:
            data["scrape_config_files"].append(file)

    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.delete("/scrape_config_files", tags=["Scrape Config Files"])
async def delete_scrape_config_files(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    scrape_config_files: ScrapeConfigFiles,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ScrapeConfigFiles:
    """Get the Prometheus scrape configurations."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)

    for file in scrape_config_files["scrape_config_files"]:
        if file in data["scrape_config_files"]:
            data["scrape_config_files"].remove(file)

    return await save_config_part(data, request, prom, sort_keys=sort_keys)


@router.get("/alerting", tags=["Alerting"])
async def get_alerting_config(
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
) -> AlertingConfig:
    """Get the Prometheus alerting configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    return data["alerting"]


@router.patch("/alerting", tags=["Alerting"])
async def update_alerting_config(
    request: Request,
    prom: Annotated[PrometheusAPIClient, Depends(prometheus_client, use_cache=True)],
    config: AlertingConfig,
    *,
    sort_keys: bool = Query(default=False, description="Sort YAML keys when writing the configuration"),
) -> ConfigPartResponse:
    """Update the Prometheus alerting configuration."""
    cfg_status, status_code, data = prom.get_config()
    if not cfg_status:
        return JSONResponse(content=data, status_code=status_code)
    data.update({"alerting": config.dict()})
    return await save_config_part(data, request, prom, sort_keys=sort_keys)
