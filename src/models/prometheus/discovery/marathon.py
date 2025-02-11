from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.auth import AuthorizationConfig, BasicAuthConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig


class MarathonConfig(BaseModel):
    """
    Marathon SD configurations allow retrieving scrape targets using the Marathon REST API.
    Prometheus will periodically check the REST endpoint for currently running tasks and
    create a target group for every app that has at least one healthy task.
    ref: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#marathon_sd_config
    """

    servers: list[str] = Field(
        ...,
        description="List of URLs to be used to contact Marathon servers. You need to provide at least one server URL.",
    )
    refresh_interval: str | None = Field("30s", description="Polling interval. Default is 30 seconds.")
    auth_token: SecretStr | None = Field(
        None,
        description="Optional authentication information for token-based authentication. "
        "Mutually exclusive with auth_token_file and other authentication mechanisms.",
    )
    auth_token_file: str | None = Field(
        None,
        description="Optional authentication information for token-based authentication. "
        "Mutually exclusive with auth_token and other authentication mechanisms.",
    )
    basic_auth: BasicAuthConfig | None = Field(
        None,
        description="Sets the Authorization header on every request with the configured username and password. "
        "Mutually exclusive with other authentication mechanisms.",
    )
    authorization: AuthorizationConfig | None = Field(
        None,
        description="Optional Authorization header configuration. Current version of DC/OS marathon does not "
        "support standard Authentication header, use auth_token or auth_token_file instead.",
    )
    oauth2: OAuth2Config | None = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.",
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2. Default is true.")
    tls_config: TLSConfig | None = Field(None, description="TLS configuration for connecting to Marathon servers.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be "
        "excluded from proxying. IP and domain names can contain port numbers.",
    )
    proxy_from_environment: bool | None = Field(
        False, description="Use proxy URL indicated by environment variables. Default is false."
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
