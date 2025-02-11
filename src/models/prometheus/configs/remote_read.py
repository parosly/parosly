from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc import auth, tls


class RemoteReadConfig(BaseModel):
    url: str = Field(..., description="The URL of the endpoint to query from.")
    name: str | None = Field(
        default=None,
        description="Name of the remote read config, which if specified must be unique among remote read configs. "
        "The name will be used in metrics and logging in place of a generated value to help users "
        "distinguish between remote read configs.",
    )
    required_matchers: dict[str, str] | None = Field(
        default=None,
        description="An optional list of equality matchers which have to be present in a selector to query the "
        "remote read endpoint.",
    )
    remote_timeout: str | None = Field("1m", description="Timeout for requests to the remote read endpoint.")
    headers: dict[str, str] | None = Field(
        default=None,
        description="Custom HTTP headers to be sent along with each remote read request. Be aware that headers "
        "that are set by Prometheus itself can't be overwritten.",
    )
    read_recent: bool | None = Field(
        default=False,
        description="Whether reads should be made for queries for time ranges that the local storage should have "
        "complete data for.",
    )
    basic_auth: auth.BasicAuthConfig | None = Field(
        default=None,
        description="Sets the `Authorization` header on every remote read request with the configured username and "
        "password. password and password_file are mutually exclusive.",
    )
    authorization: auth.AuthorizationConfig | None = Field(
        default=None, description="Optional `Authorization` header configuration."
    )
    oauth2: auth.OAuth2Config | None = Field(
        default=None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth or authorization.",
    )
    tls_config: tls.TLSConfig | None = Field(default=None, description="Configures the remote read request's TLS settings.")
    proxy_url: str | None = Field(default=None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        default=None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded "
        "from proxying. IP and domain names can contain port numbers.",
    )
    proxy_from_environment: bool | None = Field(
        default=False,
        description="Use proxy URL indicated by environment variables (HTTP_PROXY, https_proxy, HTTPs_PROXY, "
        "https_proxy, and no_proxy).",
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        default=None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        default=True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(default=True, description="Whether to enable HTTP2.")
    filter_external_labels: bool | None = Field(
        default=True, description="Whether to use the external labels as selectors for the remote read endpoint."
    )
