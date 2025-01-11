from pydantic import BaseModel, ConfigDict


class BaseBlock(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class DataBlock(BaseBlock):
    pass
