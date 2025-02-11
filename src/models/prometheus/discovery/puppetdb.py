from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.auth import AuthorizationConfig, BasicAuthConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig


class PuppetDBSDConfig(BaseModel):
    """
    PuppetDB SD configurations allow retrieving scrape targets from PuppetDB resources.
    This SD discovers resources and will create a target for each resource returned by the API.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#puppetdb_sd_config
    """

    url: str = Field(..., description="The URL of the PuppetDB root query endpoint.")
    query: str = Field(
        ...,
        description="Puppet Query Language (PQL) query. Only resources are supported. "
        "https://puppet.com/docs/puppetdb/latest/api/query/v4/pql.html",
    )
    include_parameters: bool | None = Field(
        False,
        description="Whether to include the parameters as meta labels. Note: Enabling this exposes "
        "parameters in the Prometheus UI and API.",
    )
    refresh_interval: str | None = Field(
        "60s", description="Refresh interval to re-read the resources list. Default is 60 seconds."
    )
    port: int | None = Field(80, description="The port to scrape metrics from. Default is 80.")
    tls_config: TLSConfig | None = Field(None, description="TLS configuration to connect to the PuppetDB.")
    basic_auth: BasicAuthConfig | None = Field(None, description="Optional HTTP basic authentication information.")
    authorization: AuthorizationConfig | None = Field(None, description="Authorization HTTP header configuration.")
    oauth2: OAuth2Config | None = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.",
    )
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names "
        "that should be excluded from proxying.",
    )
    proxy_from_environment: bool | None = Field(
        False, description="Use proxy URL indicated by environment variables. Default is false."
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2. Default is true.")
