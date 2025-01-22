from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import CustomerResponse, CustomerUpdate, CustomerCreate
from typing import List
from crud import (
    create_customer,
    get_customers,
    get_customer,
    delete_customer,
    update_customer,
)

router = APIRouter()

@router.get("/")
def read_root():
    """
    Root endpoint of the API.

    """
    return {"message": "Stock Menagement API"}

@router.get("/customers/", response_model=List[CustomerResponse])
def read_all_customers_route(db: Session = Depends(get_db)):
    """
    Retrieve all customers from the database.

    """
    customers = get_customers(db)
    return customers

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def read_one_customer_route(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific customer by its ID.

    """
    customer = get_customer(db=db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers/", response_model=CustomerResponse)
def create_customer_route(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer in the database.

    """
    return create_customer(db=db, customer=customer)

@router.delete("/customers/{customer_id}", response_model=CustomerResponse)
def delete_customer_route(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer from the database by its ID.

    """
    customer_db = delete_customer(db=db, customer_id=customer_id)
    if customer_db is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_db

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer_route(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update an existing customer in the database.

    """
    customer_db = update_customer(db=db, customer_id=customer_id, customer=customer)
    if customer_db is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_db