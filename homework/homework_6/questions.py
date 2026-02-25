from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ConfigDict
)

__all__ = [
    'QuestionBase',
    'QuestionCreateRequest',
    'QuestionUpdateRequest',
    'QuestionRetrive',
    'QuestionList',
    'QuestionCreateResponse'
]

from models import Question


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid"
    )


class CategoryBase(BaseSchema):
    id: int
    name: str

class QuestionBase(BaseSchema):
    title: str = Field(..., min_length= 15, max_length=150)
    description: str | None = Field(default=None, min_length= 20, max_length=750)
    start_date: datetime
    end_date: datetime
    category_id: int | None = None

    @model_validator(mode="after")
    def validate_after(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date must be before end date")

        return self

class QuestionCreateRequest(BaseSchema):
    ...


class QuestionUpdateRequest(BaseSchema):
    title: str | None = Field(default=None, min_length= 15, max_length=150)
    description: str | None = Field(default=None, min_length= 20, max_length=750)
    start_date: datetime | None
    end_date: datetime | None
    is_active: bool | None
    category_id: int | None = None

    @model_validator(mode="after")
    def validate_after(self):
        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date:
                raise ValueError("Start date must be before end date")
        return self

class QuestionRetrive(QuestionBase):
    id: int
    is_active: bool
    category_id: int | None = None

class QuestionList(BaseSchema):
    id: int
    title: str
    start_date: datetime
    is_active: bool
    category_id: int | None = None

class QuestionCreateResponse(QuestionRetrive):
    ...