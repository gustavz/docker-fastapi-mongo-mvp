from typing import Any, Callable, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from app.constants import EXAMPLE_ID


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_value(value: str | ObjectId) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("invalid ID")
            return ObjectId(value)

        schema = core_schema.no_info_plain_validator_function(validate_value)
        return core_schema.json_or_python_schema(json_schema=schema, python_schema=schema)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class MongoModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default_factory=ObjectId, alias="_id", examples=[EXAMPLE_ID]
    )

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class Item(MongoModel):
    name: str
    description: str
    value: float