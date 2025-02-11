from pydantic import BaseModel, Field


class ServersetSDConfig(BaseModel):
    """
    Serverset SD configurations allow retrieving scrape targets from Serversets which are stored in Zookeeper.
    Serversets are commonly used by Finagle and Aurora.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#serverset_sd_config
    """

    servers: list[str] = Field(..., description="The Zookeeper servers.")
    paths: list[str] = Field(
        ..., description="Paths can point to a single serverset, or the root of a tree of serversets."
    )
    timeout: str | None = Field(
        "10s", description="Timeout for connections to Zookeeper servers. Default is 10 seconds."
    )
