from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc import auth, tls


class ConsulSDConfig(BaseModel):
    """
    Consul SD configurations allow retrieving scrape targets from Consul's Catalog API.

    The following meta labels are available on targets during relabeling:

    __meta_consul_address: the address of the target
    __meta_consul_dc: the datacenter name for the target
    __meta_consul_health: the health status of the service
    __meta_consul_partition: the admin partition name where the service is registered
    __meta_consul_metadata_<key>: each node metadata key value of the target
    __meta_consul_node: the node name defined for the target
    __meta_consul_service_address: the service address of the target
    __meta_consul_service_id: the service ID of the target
    __meta_consul_service_metadata_<key>: each service metadata key value of the target
    __meta_consul_service_port: the service port of the target
    __meta_consul_service: the name of the service the target belongs to
    __meta_consul_tagged_address_<key>: each node tagged address key value of the target
    __meta_consul_tags: the list of tags of the target joined by the tag separator
    """

    server: str | None = Field("localhost:8500", description="The Consul server address.")
    path_prefix: str | None = Field(
        None, description="Prefix for URIs when Consul is behind an API gateway (reverse proxy)."
    )
    token: SecretStr | None = Field(None, description="The token for accessing Consul API.")
    datacenter: str | None = Field(None, description="The datacenter to use.")
    namespace: str | None = Field(None, description="Namespace for Consul Enterprise.")
    partition: str | None = Field(None, description="Admin partition for Consul Enterprise.")
    scheme: str | None = Field("http", description="The scheme to use for requests (http or https).")
    username: str | None = Field(None, description="Deprecated: Use basic_auth instead.")
    password: SecretStr | None = Field(None, description="Deprecated: Use basic_auth instead.")
    services: list[str] | None = Field(
        None, description="A list of services for which targets are retrieved. If omitted, all services are scraped."
    )
    tags: list[str] | None = Field(
        None,
        description="An optional list of tags used to filter nodes for a given service. "
        "Services must contain all tags in the list.",
    )
    node_meta: dict[str, str] | None = Field(
        None, description="Node metadata key/value pairs to filter nodes for a given service."
    )
    tag_separator: str | None = Field(",", description="The string by which Consul tags are joined into the tag label.")
    allow_stale: bool | None = Field(True, description="Allow stale Consul results.")
    refresh_interval: str | None = Field("30s", description="The time after which the provided names are refreshed.")
    basic_auth: auth.BasicAuthConfig | None = Field(None, description="Optional HTTP basic authentication information.")
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Optional `Authorization` header configuration."
    )
    oauth2: auth.OAuth2Config | None = Field(None, description="Optional OAuth 2.0 configuration.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, "
        "domain names that should be excluded from proxying.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")
    tls_config: tls.TLSConfig | None = Field(None, description="TLS configuration.")
