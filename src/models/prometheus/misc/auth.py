from pydantic import BaseModel, Field, SecretStr

from src.models.prometheus.misc import tls


class BasicAuthConfig(BaseModel):
    username: str | None = Field(None)
    password: SecretStr | None = Field(None)
    password_file: str | None = Field(None)


class AuthorizationConfig(BaseModel):
    type: str | None = Field("Bearer")
    credentials: SecretStr | None = Field(None)
    credentials_file: str | None = Field(None)


class OAuth2Config(BaseModel):
    client_id: str = Field(..., description="The client ID.")
    client_secret: SecretStr | None = Field(None, description="The client secret.")
    client_secret_file: str | None = Field(
        None, description="The client secret file. It is mutually exclusive with `client_secret`."
    )
    scopes: list[str] | None = Field(None, description="Scopes for the token request.")
    token_url: str = Field(..., description="The URL to fetch the token from.")
    endpoint_params: dict[str, str] | None = Field(None, description="Optional parameters to append to the token URL.")
    tls_config: tls.TLSConfig | None = Field(None, description="Configures the token request's TLS settings.")
    proxy_url: str | None = Field(None, description="Optional proxy URL.")
    no_proxy: str | None = Field(
        None,
        description="Comma-separated string that can contain IPs, CIDR notation, domain names that should be "
        "excluded from proxying. IP and domain names can contain port numbers.",
    )
    proxy_from_environment: bool | None = Field(False, description="Use proxy URL indicated by environment variables.")
    proxy_connect_header: dict[str, list[SecretStr]] | None = Field(
        None, description="Specifies headers to send to proxies during CONNECT requests."
    )


class Sigv4Config(BaseModel):
    region: str | None = Field(None)
    access_key: str | None = Field(None)
    secret_key: SecretStr | None = Field(None)
    profile: str | None = Field(None)
    role_arn: str | None = Field(None)


class ManagedIdentityConfig(BaseModel):
    client_id: str | None = Field(None)


class AzureOAuthConfig(BaseModel):
    client_id: str | None = Field(None)
    client_secret: SecretStr | None = Field(None)
    tenant_id: str | None = Field(None)


class AzureSDKConfig(BaseModel):
    tenant_id: str | None = Field(None)


class AzureADConfig(BaseModel):
    cloud: str | None = Field("AzurePublic")
    managed_identity: ManagedIdentityConfig | None = Field(None)
    oauth: AzureOAuthConfig | None = Field(None)
    sdk: AzureSDKConfig | None = Field(None)
