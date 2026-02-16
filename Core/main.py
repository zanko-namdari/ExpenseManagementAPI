from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from core.database import get_db, Transaction
from core.schemas import ExpenseOutSchema, ExpenseCreateUpdateSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(
    title="Expense Management API",
    description="API for managing expenses",
    version="1.0.0",
    lifespan=lifespan,
)

# ------------------------
# Create Expense
# ------------------------
@app.post(
    "/expenses",
    response_model=ExpenseOutSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense: ExpenseCreateUpdateSchema,
    db: Session = Depends(get_db),
):
    new_expense = Transaction(
        description=expense.description,
        amount=expense.amount,
        type="expense",
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# ------------------------
# Read All Expenses
# ------------------------
@app.get("/expenses", response_model=list[ExpenseOutSchema])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.type == "expense").all()


# ------------------------
# Read One Expense
# ------------------------
@app.get("/expenses/{expense_id}", response_model=ExpenseOutSchema)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Transaction).filter(
        Transaction.id == expense_id,
        Transaction.type == "expense"
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


# ------------------------
# Update Expense
# ------------------------
@app.put("/expenses/{expense_id}", response_model=ExpenseOutSchema)
def update_expense(
    expense_id: int,
    data: ExpenseCreateUpdateSchema,
    db: Session = Depends(get_db),
):
    expense = db.query(Transaction).filter(
        Transaction.id == expense_id,
        Transaction.type == "expense"
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.description = data.description
    expense.amount = data.amount

    db.commit()
    db.refresh(expense)

    return expense


# ------------------------
# Delete Expense
# ------------------------
@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Transaction).filter(
        Transaction.id == expense_id,
        Transaction.type == "expense"
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
