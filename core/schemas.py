from pydantic import BaseModel, field_validator


class BasePersonSchema(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("Name must not exceed 32 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value

class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):
    id: int


class PersonUpdateSchema(BasePersonSchema):
    pass
