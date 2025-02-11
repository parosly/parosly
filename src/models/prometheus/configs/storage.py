from pydantic import BaseModel, Field

from ..misc.exemplar import ExemplarsConfig
from ..misc.tsdb import TSDBConfig


class StorageConfig(BaseModel):
    tsdb: TSDBConfig | None = Field(None)
    exemplars: ExemplarsConfig | None = Field(None)
