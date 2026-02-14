from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict


app=FastAPI(title="Expense Management API", description="API for managing expenses", version="1.0.0")

expenses: Dict[int, dict] = {}
current_id = 1


class Expense(BaseModel):
    description: str
    amount: float


class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float


# ------------------------
# Create - POST
# ------------------------
@app.post("/expenses", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense):
    global current_id

    new_expense = {
        "id": current_id,
        "description": expense.description,
        "amount": expense.amount
    }

    expenses[current_id] = new_expense
    current_id += 1

    return new_expense


# ------------------------
# Read All - GET
# ------------------------
@app.get("/expenses", response_model=list[ExpenseOut])
def get_expenses():
    return list(expenses.values())


# ------------------------
# Read One - GET by ID
# ------------------------
@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expenses[expense_id]


# ------------------------
# Update - PUT
# ------------------------
@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount
    }

    expenses[expense_id] = updated
    return updated

# ------------------------
# Delete - DELETE
# ------------------------
@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    del expenses[expense_id]