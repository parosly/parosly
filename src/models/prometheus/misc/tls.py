from pydantic import BaseModel, Field, SecretStr


class TLSConfig(BaseModel):
    ca: str | None = Field(
        None,
        description="CA certificate to validate API server certificate with. At most one of ca and ca_file is allowed.",
    )
    ca_file: str | None = Field(
        None,
        description="CA certificate file to validate API server certificate with. "
        "At most one of ca and ca_file is allowed.",
    )
    cert: str | None = Field(
        None,
        description="Certificate for client cert authentication to the server. "
        "At most one of cert and cert_file is allowed.",
    )
    cert_file: str | None = Field(
        None,
        description="Certificate file for client cert authentication to the server. "
        "At most one of cert and cert_file is allowed.",
    )
    key: SecretStr | None = Field(
        None,
        description="Key for client cert authentication to the server. At most one of key and key_file is allowed.",
    )
    key_file: str | None = Field(
        None,
        description="Key file for client cert authentication to the server. "
        "At most one of key and key_file is allowed.",
    )
    server_name: str | None = Field(None, description="ServerName extension to indicate the name of the server.")
    insecure_skip_verify: bool | None = Field(None, description="Disable validation of the server certificate.")
    min_version: str | None = Field(
        None,
        description="Minimum acceptable TLS version. "
        "Accepted values: TLS10 (TLS 1.0), TLS11 (TLS 1.1), TLS12 (TLS 1.2), TLS13 (TLS 1.3).",
    )
    max_version: str | None = Field(
        None,
        description="Maximum acceptable TLS version. "
        "Accepted values: TLS10 (TLS 1.0), TLS11 (TLS 1.1), TLS12 (TLS 1.2), TLS13 (TLS 1.3).",
    )
