import json
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class Address(BaseModel):
    city: str
    street: str
    house_number: int = Field(gt=0)

    @model_validator(mode="after")
    def check_lengths(self):
        if len(self.city) < 2:
            raise ValueError("city: минимум 2 символа")
        if len(self.street) < 3:
            raise ValueError("street: минимум 3 символа")
        return self


class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v) < 2 or not v.replace(" ", "").isalpha():
            raise ValueError("name: минимум 2 буквы, только буквы и пробелы")
        return v

    @model_validator(mode="after")
    def check_age_employment(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "если is_employed = true, возраст должен быть от 18 до 65"
            )
        return self


def process_user_registration(json_str: str) -> str:
    data = json.loads(json_str)
    user = User(**data)
    return user.model_dump_json(ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 1. УСПЕШНО: взрослый работающий
    json_ok_employed_30 = """{
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "NY",
            "street": "Main Street",
            "house_number": 10
        }
    }"""

    # 2. УСПЕШНО: неработающий ребёнок
    json_ok_child_unemployed = """{
        "name": "Alice",
        "age": 12,
        "email": "alice@example.com",
        "is_employed": false,
        "address": {
            "city": "LA",
            "street": "Sunset Blvd",
            "house_number": 5
        }
    }"""

    # 3. ОШИБКА: возраст слишком большой для is_employed = true
    json_bad_age_too_old_employed = """{
        "name": "John Doe",
        "age": 70,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    # 4. ОШИБКА: имя содержит цифры
    json_bad_name_with_digits = """{
        "name": "John123",
        "age": 25,
        "email": "john123@example.com",
        "is_employed": true,
        "address": {
            "city": "Seattle",
            "street": "Pine Street",
            "house_number": 8
        }
    }"""

    # 5. ОШИБКА: отрицательный номер дома
    json_bad_house_negative = """{
        "name": "Mike",
        "age": 35,
        "email": "mike@example.com",
        "is_employed": true,
        "address": {
            "city": "Paris",
            "street": "Central Street",
            "house_number": -10
        }
    }"""

    examples = [
        ("OK: взрослый работающий", json_ok_employed_30),
        ("OK: неработающий ребёнок", json_ok_child_unemployed),
        ("BAD: возраст 70 и is_employed=true", json_bad_age_too_old_employed),
        ("BAD: имя с цифрами", json_bad_name_with_digits),
        ("BAD: отрицательный номер дома", json_bad_house_negative),
    ]

    for title, js in examples:
        print("=" * 80)
        print(title)
        try:
            result = process_user_registration(js)
            print("ВАЛИДАЦИЯ УСПЕШНА, результат JSON:")
            print(result)
        except ValidationError as e:
            print("ОШИБКИ ВАЛИДАЦИИ:")
            print(e)