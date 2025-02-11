from pydantic import BaseModel, Field


class RuntimeConfig(BaseModel):
    gogc: int | None = Field(
        75,
        description="Configure the Go garbage collector GOGC parameter See: https://tip.golang.org/doc/gc-guide#GOGC "
        "Lowering this number increases CPU usage.",
    )
