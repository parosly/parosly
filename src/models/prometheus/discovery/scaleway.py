from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.tls import TLSConfig


class ScalewaySDConfig(BaseModel):
    """
    Scaleway SD configurations allow retrieving scrape targets from Scaleway instances and baremetal services.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scaleway_sd_config
    """

    access_key: str = Field(..., description="Access key to use. https://console.scaleway.com/project/credentials")
    secret_key: SecretStr | None = Field(
        None, description="Secret key to use when listing targets. Mutually exclusive with secret_key_file."
    )
    secret_key_file: str | None = Field(
        None, description="File containing the secret key. Mutually exclusive with secret_key."
    )
    project_id: str = Field(..., description="Project ID of the targets.")
    role: str = Field(..., description="Role of the targets to retrieve. Must be 'instance' or 'baremetal'.")
    port: int | None = Field(80, description="The port to scrape metrics from. Default is 80.")
    api_url: str | None = Field(
        "https://api.scaleway.com",
        description="API URL to use when doing the server listing requests. Default is 'https://api.scaleway.com'.",
    )
    zone: str | None = Field(
        "fr-par-1", description="Zone is the availability zone of your targets (e.g. fr-par-1). Default is 'fr-par-1'."
    )
    name_filter: str | None = Field(
        None, description="Name filter (works as a LIKE) to apply on the server listing request."
    )
    tags_filter: list[str] | None = Field(
        None,
        description="Tag filter (a server needs to have all defined tags to be listed) to apply on the server listing request.",
    )
    refresh_interval: str | None = Field(
        "60s", description="Refresh interval to re-read the targets list. Default is 60 seconds."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2. Default is true.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying.",
    )
    proxy_from_environment: bool | None = Field(
        False, description="Use proxy URL indicated by environment variables. Default is false."
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Headers to send to proxies during CONNECT requests."
    )
    tls_config: TLSConfig | None = Field(None, description="TLS configuration settings.")
