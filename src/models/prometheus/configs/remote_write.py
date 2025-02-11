from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.configs import relabel
from src.models.prometheus.misc import auth, tls


class QueueConfig(BaseModel):
    capacity: int | None = Field(10000)
    max_shards: int | None = Field(50)
    min_shards: int | None = Field(1)
    max_samples_per_send: int | None = Field(2000)
    batch_send_deadline: str | None = Field("5s")
    min_backoff: str | None = Field("30ms")
    max_backoff: str | None = Field("5s")
    retry_on_http_429: bool | None = Field(False)
    sample_age_limit: str | None = Field("0s")


class MetadataConfig(BaseModel):
    send: bool | None = Field(True)
    send_interval: str | None = Field("1m")
    max_samples_per_send: int | None = Field(500)


class RemoteWriteConfig(BaseModel):
    url: str = Field(..., description="The URL of the endpoint to send samples to.")
    remote_timeout: str | None = Field("30s", description="Timeout for requests to the remote write endpoint.")
    headers: dict[str, str] | None = Field(
        None,
        description="Custom HTTP headers to be sent along with each remote write request. Be aware that headers "
        "that are set by Prometheus itself can't be overwritten.",
    )
    write_relabel_configs: list[relabel.RelabelConfig] | None = Field(
        None, description="List of remote write relabel configurations."
    )
    name: str | None = Field(
        None,
        description="Name of the remote write config, which if specified must be unique among remote write configs. "
        "The name will be used in metrics and logging in place of a generated value to help users "
        "distinguish between remote write configs.",
    )
    send_exemplars: bool | None = Field(
        False,
        description="Enables sending of exemplars over remote write. Note that exemplar storage itself must be enabled "
        "for exemplars to be scraped in the first place.",
    )
    send_native_histograms: bool | None = Field(
        False, description="Enables sending of native histograms, also known as sparse histograms, over remote write."
    )
    basic_auth: auth.BasicAuthConfig | None = Field(
        None,
        description="Sets the `Authorization` header on every remote write request with the configured username and "
        "password. password and password_file are mutually exclusive.",
    )
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Optional `Authorization` header configuration."
    )
    sigv4: auth.Sigv4Config | None = Field(
        None,
        description="Optionally configures AWS's Signature Verification 4 signing process to sign requests. "
        "Cannot be set at the same time as basic_auth, authorization, oauth2, or azuread. To use the "
        "default credentials from the AWS SDK, use `sigv4: {}`.",
    )
    oauth2: auth.OAuth2Config | None = Field(
        None,
        description="Optional OAuth 2.0 configuration. Cannot be used at the same time as basic_auth, authorization, "
        "sigv4, or azuread.",
    )
    azuread: auth.AzureADConfig | None = Field(
        None,
        description="Optional AzureAD configuration. Cannot be used at the same time as basic_auth, authorization, "
        "oauth2, or sigv4.",
    )
    tls_config: tls.TLSConfig | None = Field(None, description="Configures the remote write request's TLS settings.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be "
        "excluded from proxying. IP and domain names can contain port numbers.",
    )
    proxy_from_environment: bool | None = Field(
        False,
        description="Use proxy URL indicated by environment variables (HTTP_PROXY, https_proxy, HTTPs_PROXY, "
        "https_proxy, and no_proxy).",
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")
    queue_config: QueueConfig | None = Field(None, description="Configures the queue used to write to remote storage.")
    metadata_config: MetadataConfig | None = Field(
        None,
        description="Configures the sending of series metadata to remote storage. Metadata configuration is subject "
        "to change at any point or be removed in future releases.",
    )
