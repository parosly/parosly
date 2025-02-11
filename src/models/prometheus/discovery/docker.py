from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc import auth, tls


class DockerSDConfig(BaseModel):
    """
    Docker SD configurations allow retrieving scrape targets from Docker Engine hosts.

    This SD discovers "containers" and will create a target for each network IP and port
    the container is configured to expose.

    Available meta labels:

    __meta_docker_container_id: the id of the container
    __meta_docker_container_name: the name of the container
    __meta_docker_container_network_mode: the network mode of the container
    __meta_docker_container_label_<labelname>: each label of the container, with any
    unsupported characters converted to an underscore
    __meta_docker_network_id: the ID of the network
    __meta_docker_network_name: the name of the network
    __meta_docker_network_ingress: whether the network is ingress
    __meta_docker_network_internal: whether the network is internal
    __meta_docker_network_label_<labelname>: each label of the network, with any
    unsupported characters converted to an underscore
    __meta_docker_network_scope: the scope of the network
    __meta_docker_network_ip: the IP of the container in this network
    __meta_docker_port_private: the port on the container
    __meta_docker_port_public: the external port if a port-mapping exists
    __meta_docker_port_public_ip: the public IP if a port-mapping exists
    """

    host: str = Field(..., description="Address of the Docker daemon.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that "
        "should be excluded from proxying.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    tls_config: tls.TLSConfig | None = Field(None, description="TLS configuration.")
    port: int | None = Field(
        80,
        description="The port to scrape metrics from, when `role` is nodes, and for discovered tasks "
        "and services that don't have published ports.",
    )
    host_networking_host: str | None = Field(
        "localhost", description="The host to use if the container is in host networking mode."
    )
    filters: list[dict[str, list[str]]] | None = Field(
        None, description="Optional filters to limit the discovery process to a subset of available resources."
    )
    refresh_interval: str | None = Field("60s", description="The time after which the containers are refreshed.")
    basic_auth: auth.BasicAuthConfig | None = Field(None, description="Optional HTTP basic authentication information.")
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Optional `Authorization` header configuration."
    )
    oauth2: auth.OAuth2Config | None = Field(None, description="Optional OAuth 2.0 configuration.")
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")


class DockerSwarmSDConfig(BaseModel):
    host: str = Field(..., description="Address of the Docker daemon.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that "
        "should be excluded from proxying.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )
    tls_config: tls.TLSConfig | None = Field(None, description="TLS configuration.")
    role: str = Field(..., description="Role of the targets to retrieve. Must be `services`, `tasks`, or `nodes`.")
    port: int | None = Field(
        80,
        description="The port to scrape metrics from, when `role` is nodes, and for discovered tasks and "
        "services that don't have published ports.",
    )
    filters: list[dict[str, list[str]]] | None = Field(
        None, description="Optional filters to limit the discovery process to a subset of available resources."
    )
    refresh_interval: str | None = Field(
        "60s", description="The time after which the service discovery data is refreshed."
    )
    basic_auth: auth.BasicAuthConfig | None = Field(None, description="Optional HTTP basic authentication information.")
    authorization: auth.AuthorizationConfig | None = Field(
        None, description="Optional `Authorization` header configuration."
    )
    oauth2: auth.OAuth2Config | None = Field(None, description="Optional OAuth 2.0 configuration.")
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2.")
