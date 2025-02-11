from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.auth import AuthorizationConfig, BasicAuthConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig


class NomadSDConfig(BaseModel):
    """
    Nomad SD configurations allow retrieving scrape targets from Nomad's Service API.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#nomad_sd_config
    """

    allow_stale: bool | None = Field(True, description="Allow stale reads. Default is true.")
    namespace: str | None = Field("default", description="The Nomad namespace. Default is 'default'.")
    refresh_interval: str | None = Field(
        "60s", description="Refresh interval to re-read the instance list. Default is 60 seconds."
    )
    region: str | None = Field("global", description="The Nomad region. Default is 'global'.")
    server: str | None = Field(None, description="The Nomad server address.")
    tag_separator: str | None = Field(
        ",", description="The string by which Nomad tags are joined into the tag label. Default is ','."
    )
    basic_auth: BasicAuthConfig | None = Field(None, description="Optional HTTP basic authentication information.")
    authorization: AuthorizationConfig | None = Field(None, description="Optional Authorization header configuration.")
    oauth2: OAuth2Config | None = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.",
    )
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, "
        "domain names that should be excluded from proxying.",
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
    tls_config: TLSConfig | None = Field(None, description="TLS configuration settings.")
