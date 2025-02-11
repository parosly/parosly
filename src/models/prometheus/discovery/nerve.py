from pydantic import BaseModel, Field


class NerveSDConfig(BaseModel):
    """
    Nerve SD configurations allow retrieving scrape targets from AirBnB's Nerve which are stored in Zookeeper.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#nerve_sd_config
    """

    servers: list[str] = Field(..., description="The Zookeeper servers.")
    paths: list[str] = Field(..., description="Paths can point to a single service, or the root of a tree of services.")
    timeout: str | None = Field(
        "10s", description="Timeout for connections to Zookeeper servers. Default is 10 seconds."
    )
