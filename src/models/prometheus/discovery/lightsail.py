from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc.auth import AuthorizationConfig, BasicAuthConfig, OAuth2Config
from src.models.prometheus.misc.tls import TLSConfig


class LightsailAPIConfig(BaseModel):
    """
    Lightsail SD configurations allow retrieving scrape targets from AWS Lightsail instances. The
    private IP address is used by default, but may be changed to the public IP address with relabeling.

    The following meta labels are available on targets during relabeling:

    __meta_lightsail_availability_zone: the availability zone in which the instance is running
    __meta_lightsail_blueprint_id: the Lightsail blueprint ID
    __meta_lightsail_bundle_id: the Lightsail bundle ID
    __meta_lightsail_instance_name: the name of the Lightsail instance
    __meta_lightsail_instance_state: the state of the Lightsail instance
    __meta_lightsail_instance_support_code: the support code of the Lightsail instance
    __meta_lightsail_ipv6_addresses: comma separated list of IPv6 addresses assigned to the instance's
    network interfaces, if present
    __meta_lightsail_private_ip: the private IP address of the instance
    __meta_lightsail_public_ip: the public IP address of the instance, if available
    __meta_lightsail_region: the region of the instance
    __meta_lightsail_tag_<tagkey>: each tag value of the instance
    """

    region: str | None = Field(
        None, description="The AWS region. If blank, the region from the instance metadata is used."
    )
    endpoint: str | None = Field(None, description="Custom endpoint to be used.")
    access_key: str | None = Field(
        None, description="The AWS access key. If blank, the environment variable AWS_ACCESS_KEY_ID is used."
    )
    secret_key: SecretStr | None = Field(
        None, description="The AWS secret key. If blank, the environment variable AWS_SECRET_ACCESS_KEY is used."
    )
    profile: str | None = Field(None, description="Named AWS profile used to connect to the API.")
    role_arn: str | None = Field(None, description="AWS Role ARN, an alternative to using AWS API keys.")
    refresh_interval: str | None = Field(
        "60s", description="Refresh interval to re-read the instance list. Default is 60 seconds."
    )
    port: int | None = Field(80, description="The port to scrape metrics from. Default is 80.")
    basic_auth: BasicAuthConfig | None = Field(
        None, description="Optional HTTP basic authentication information, currently not supported by AWS."
    )
    authorization: AuthorizationConfig | None = Field(
        None, description="Optional Authorization header configuration, currently not supported by AWS."
    )
    oauth2: OAuth2Config | None = Field(
        None, description="Optional OAuth 2.0 configuration, currently not supported by AWS."
    )
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None, description="Comma-separated string of IPs, CIDR notation, or domain names to be excluded from proxying."
    )
    proxy_from_environment: bool | None = Field(
        False, description="Use proxy URL indicated by environment variables. Default is false."
    )
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Headers to send to proxies during CONNECT requests."
    )
    follow_redirects: bool | None = Field(
        True, description="Configure whether HTTP requests follow HTTP 3xx redirects. Default is true."
    )
    enable_http2: bool | None = Field(True, description="Whether to enable HTTP2. Default is true.")
    tls_config: TLSConfig | None = Field(None, description="TLS configuration settings.")
