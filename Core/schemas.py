from pydantic import BaseModel, field_validator, field_serializer, Field

class BaseExpenseSchema(BaseModel):
    description: str = Field(..., example="Lunch at cafe")
    
    @field_validator('description')
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be empty")
        return value
    
    amount: float = Field(..., description="Amount in USD", gt=0, example=15.50)
    
    @field_validator('amount')
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value
    
    @field_serializer('amount')
    def serialize_amount(self, value):
        # Convert value to float before formatting
        return f"${float(value):.2f}"


class ExpenseOutSchema(BaseExpenseSchema):
    id: int = Field(..., description="Unique identifier for the expense", example=1)


class ExpenseCreateUpdateSchema(BaseExpenseSchema):
    pass
