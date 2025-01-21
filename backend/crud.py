from sqlalchemy.orm import Session
from schemas import CustomerUpdate, CustomerCreate
from models import CustomerModel

def get_customers(db: Session):
    """
    Retrieve all customers from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list: A list of all Customers in the database.
    """
    return db.query(CustomerModel).all()

def get_customers(db: Session, customer_id: int):
    """
    Retrieve a specific customer by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        customer_id (int): The ID of the customer to retrieve.

    Returns:
        CustomerModel or None: The customer with the specified ID, or None if not found.
    """
    return db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()

def create_customer(db: Session, customer: CustomerCreate):
    """
    Create a new customer in the database.

    Args:
        db (Session): SQLAlchemy database session.
        customer (CustomerCreate): An instance of CustomerCreate containing customer details.

    Returns:
        CustomerModel: The newly created customer instance.
    """
    db_customer = CustomerModel(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    """
    Delete a customer from the database by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        customer_id (int): The ID of the customer to delete.

    Returns:
        CustomerModel or None: The deleted customer instance, or None if not found.
    """
    db_customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    db.delete(db_customer)
    db.commit()
    return db_customer


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    """
    Update the details of an existing customer.

    Args:
        db (Session): SQLAlchemy database session.
        customer_id (int): The ID of the customer to update.
        customer (CustomerUpdate): An instance of CustomerUpdate containing updated customer details.

    Returns:
        CustomerModel or None: The updated customer instance, or None if the customer is not found.
    """
    db_customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()

    if db_customer is None:
        return None

    if customer.name is not None:
        db_customer.name = customer.name
    if customer.description is not None:
        db_customer.description = customer.description
    if customer.price is not None:
        db_customer.price = customer.price
    if customer.category is not None:
        db_customer.category = customer.category
    if customer.supplier_email is not None:
        db_customer.supplier_email = customer.supplier_email

    db.commit()
    return db_customer