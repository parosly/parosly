from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.auth import AuthorizationConfig, BasicAuthConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig


class IONOSCloudConfig(BaseModel):
    """
    IONOS SD configurations allows retrieving scrape targets from IONOS Cloud API.
    This service discovery uses the first NICs IP address by default, but that can
    be changed with relabeling. The following meta labels are available on all
    targets during relabeling:

    __meta_ionos_server_availability_zone: the availability zone of the server
    __meta_ionos_server_boot_cdrom_id: the ID of the CD-ROM the server is booted from
    __meta_ionos_server_boot_image_id: the ID of the boot image or snapshot the server is booted from
    __meta_ionos_server_boot_volume_id: the ID of the boot volume
    __meta_ionos_server_cpu_family: the CPU family of the server to
    __meta_ionos_server_id: the ID of the server
    __meta_ionos_server_ip: comma separated list of all IPs assigned to the server
    __meta_ionos_server_lifecycle: the lifecycle state of the server resource
    __meta_ionos_server_name: the name of the server
    __meta_ionos_server_nic_ip_<nic_name>: comma separated list of IPs, grouped
    by the name of each NIC attached to the server
    __meta_ionos_server_servers_id: the ID of the servers the server belongs to
    __meta_ionos_server_state: the execution state of the server
    __meta_ionos_server_type: the type of the server
    """

    datacenter_id: str = Field(..., description="The unique ID of the data center.")
    basic_auth: BasicAuthConfig | None = Field(
        None,
        description="Optional HTTP basic authentication information, required when using "
        "IONOS Cloud username and password as authentication method.",
    )
    authorization: AuthorizationConfig | None = Field(
        None,
        description="Optional Authorization header configuration, required when using "
        "IONOS Cloud token as authentication method.",
    )
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
    port: int | None = Field(80, description="The port to scrape metrics from. Default is 80.")
    refresh_interval: str | None = Field(
        "60s", description="The time after which the servers are refreshed. Default is 60 seconds."
    )
