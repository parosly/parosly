from pydantic import BaseModel, Field

from src.models.prometheus.configs import relabel
from src.models.prometheus.misc import alertmanager


class AlertingConfig(BaseModel):
    alert_relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None,
        description="Dynamically rewrite the label set of a target before it gets scraped. Multiple relabeling "
        "steps can be configured per scrape configuration",
    )
    alertmanagers: list[alertmanager.AlertmanagerConfig] | None = Field(
        None, description="specifies Alertmanager instances the Prometheus server sends alerts to."
    )
