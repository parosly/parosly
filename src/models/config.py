from pydantic import BaseModel, Extra, Field

from .prometheus.configs import _globals, scrape
from .prometheus.configs.alerting import AlertingConfig
from .prometheus.configs.remote_read import RemoteReadConfig
from .prometheus.configs.remote_write import RemoteWriteConfig
from .prometheus.configs.runtime import RuntimeConfig
from .prometheus.configs.storage import StorageConfig
from .prometheus.configs.trace import TraceExporterConfig


class UpdateConfig(BaseModel, extra=Extra.allow):
    global_: _globals.GlobalConfig | None = Field(
        alias="global",
        description="The global configuration specifies parameters that are valid in all other configuration "
        "contexts. They also serve as defaults for other configuration sections.",
    )
    runtime: RuntimeConfig | None = Field()
    rule_files: list[str] | None = Field(
        description="Rule files specifies a list of globs. Rules and alerts are read from all matching files."
    )
    scrape_config_files: list[str] | None = Field(
        description="Scrape config files specifies a list of globs. Scrape "
        "configs are read from all matching files and appended to "
        "the list of scrape configs."
    )
    scrape_configs: list[scrape.ScrapeConfig] | None = Field(description="A list of scrape configurations.")
    alerting: AlertingConfig | None = Field(description="Alerting specifies settings related to the Alertmanager.")
    remote_write: list[RemoteWriteConfig] | None = Field(description="Settings related to the remote write feature.")
    remote_read: list[RemoteReadConfig] | None = Field(description="Settings related to the remote read feature.")
    storage: StorageConfig | None = Field(description="Storage related settings that are runtime reloadable.")
    tracing: TraceExporterConfig | None = Field(description="Configures exporting traces.")

    def __str__(self):
        def serialize(value):
            """
            Converts nested Pydantic models, lists, and dictionaries into serializable structures.

            Args:
                value (Any): The value to serialize. Supports Pydantic models, lists, dictionaries,
                             and other data types.

            Returns:
                Any: A serializable representation of the input:
                     - Pydantic models are converted to dictionaries.
                     - Lists and dictionaries are processed recursively.
                     - Non-serializable types are returned as-is.
            """
            if isinstance(value, BaseModel):
                return value.dict(exclude_none=True)
            if isinstance(value, list):
                return [serialize(v) for v in value]
            if isinstance(value, dict):
                return {k: serialize(v) for k, v in value.items()}
            return value

        cfg = {
            "global": serialize(self.global_),
            "runtime": serialize(self.runtime),
            "rule_files": self.rule_files,
            "scrape_config_files": self.scrape_config_files,
            "scrape_configs": serialize(self.scrape_configs),
            "alerting": serialize(self.alerting),
            "remote_write": serialize(self.remote_write),
            "remote_read": serialize(self.remote_read),
            "storage": serialize(self.storage),
            "tracing": serialize(self.tracing),
        }

        return {k: v for k, v in cfg.items() if v is not None}
