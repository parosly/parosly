from pydantic import BaseModel, Field


class ExemplarsConfig(BaseModel):
    max_exemplars: int | None = Field(
        100000,
        description="Configures the maximum size of the circular buffer used to store exemplars for all series. "
        "Resizable during runtime.",
    )
