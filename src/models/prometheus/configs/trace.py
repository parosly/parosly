from pydantic import BaseModel, Field

from src.models.prometheus.misc import tls


class TraceExporterConfig(BaseModel):
    client_type: str | None = Field(
        "grpc", description="Client used to export the traces. Options are 'http' or 'grpc'."
    )
    endpoint: str = Field(
        ..., description="Endpoint to send the traces to. Should be provided in format <host>:<port>."
    )
    sampling_fraction: float | None = Field(
        0.0, description="Sets the probability a given trace will be sampled. Must be a float from 0 through 1."
    )
    insecure: bool | None = Field(False, description="If disabled, the client will use a secure connection.")
    headers: dict[str, str] | None = Field(
        None, description="Key-value pairs to be used as headers associated with gRPC or HTTP requests."
    )
    compression: str | None = Field(
        None, description="Compression key for supported compression types. Supported compression: gzip."
    )
    timeout: str | None = Field("10s", description="Maximum time the exporter will wait for each batch export.")
    tls_config: tls.TLSConfig | None = Field(None, description="TLS configuration.")
