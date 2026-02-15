from pydantic import BaseModel, Field, field_validator, field_serializer
import re

# ------------------------
# Base schema for Expense
# ------------------------
class BaseExpenseSchema(BaseModel):
    description: str = Field(
        ...,
        example="Lunch at cafe",
        description="Description of the expense"
    )

    @field_validator('description')
    def validate_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Description cannot be empty")
        # Optional: regex to allow only certain characters
        if not re.match(r'^[\w\s.,-]+$', value):
            raise ValueError("Description contains invalid characters")
        return value

    amount: float = Field(
        ...,
        description="Amount in USD, must be greater than zero",
        gt=0,
        example=15.50
    )

    @field_validator('amount')
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value

    @field_serializer('amount')
    def serialize_amount(cls, value: float) -> str:
        # Format amount as USD string
        return f"${value:.2f}"


# ------------------------
# Schema for API output
# ------------------------
class ExpenseOutSchema(BaseExpenseSchema):
    id: int = Field(..., description="Unique identifier for the expense", example=1)


# ------------------------
# Schema for API input (create/update)
# ------------------------
class ExpenseCreateUpdateSchema(BaseExpenseSchema):
    pass
