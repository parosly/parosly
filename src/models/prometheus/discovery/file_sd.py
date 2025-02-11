from pydantic import BaseModel, Field


class FileSDConfig(BaseModel):
    """
    File-based service discovery provides a more generic way to configure static targets
    and serves as an interface to plug in custom service discovery mechanisms. It reads
    a set of files containing a list of zero or more <static_config>s. Changes to all
    defined files are detected via disk watches and applied immediately.
    """

    files: list[str] = Field(..., description="Patterns for files from which target groups are extracted.")
    refresh_interval: str | None = Field(
        "5m", description="Refresh interval to re-read the files. Default is 5 minutes."
    )
