from pydantic import BaseModel, Field


class RelabelConfig(BaseModel):
    source_labels: list[str] | None = Field(
        None,
        description="The source labels select values from existing labels. Their content is concatenated using "
        "the configured separator and matched against the configured regular expression for the "
        "replace, keep, and drop actions.",
    )
    separator: str | None = Field(";", description="Separator placed between concatenated source label values.")
    target_label: str | None = Field(
        None,
        description="Label to which the resulting value is written in a replace action. It is mandatory for replace "
        "actions. Regex capture groups are available.",
    )
    regex: str | None = Field("(.*)", description="Regular expression against which the extracted value is matched.")
    modulus: int | None = Field(None, description="Modulus to take of the hash of the source label values.")
    replacement: str | None = Field(
        "$1",
        description="Replacement value against which a regex replace is performed if the regular expression matches. "
        "Regex capture groups are available.",
    )
    action: str | None = Field("replace", description="Action to perform based on regex matching.")
