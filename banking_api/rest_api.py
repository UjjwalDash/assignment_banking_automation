from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, String, DECIMAL, DateTime, func, update, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid
from datetime import datetime
import time
from contextlib import contextmanager
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/transactions_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis for distributed locking
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Models
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(String(10), primary_key=True)
    user_id = Column(String(10), index=True)
    balance = Column(DECIMAL(15, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(10), primary_key=True)
    account_id = Column(String(10), index=True)
    transaction_type = Column(String(10))
    amount = Column(DECIMAL(15, 2), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    status = Column(String(10), default="pending")
    reference = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)

# Pydantic models
class DebitRequest(BaseModel):
    amount: float = Field(..., gt=0)
    reference: Optional[str] = None
    description: Optional[str] = None
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        return v

class TransactionResponse(BaseModel):
    transaction_id: str
    account_id: str
    type: str
    amount: float
    previous_balance: float
    new_balance: float
    reference: Optional[str] = None
    timestamp: datetime
    status: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Distributed lock implementation with Redis
@contextmanager
def acquire_lock(account_id, ttl=10):
    lock_key = f"lock:account:{account_id}"
    lock_value = str(uuid.uuid4())
    
    # Try to acquire lock
    lock_acquired = redis_client.set(lock_key, lock_value, nx=True, ex=ttl)
    
    if not lock_acquired:
        logger.warning(f"Could not acquire lock for account {account_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account is currently locked. Please try again later."
        )
    
    try:
        logger.info(f"Lock acquired for account {account_id}")
        yield
    finally:
        # Release lock if it's still the one we set
        redis_client.delete(lock_key)
        logger.info(f"Lock released for account {account_id}")

app = FastAPI(title="Transaction Processing API")

@app.post("/accounts/{account_id}/debit", response_model=TransactionResponse)
async def debit_account(
    account_id: str, 
    debit_request: DebitRequest, 
    db: Session = Depends(get_db)
):
    # Generate a transaction ID
    transaction_id = f"TX{uuid.uuid4().hex[:8].upper()}"
    
    try:
        # Acquire a distributed lock on the account
        with acquire_lock(account_id):
            # Start database transaction
            try:
                # First check if account exists and has sufficient funds
                account = db.query(Account).filter(Account.id == account_id).with_for_update().first()
                
                if not account:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Account with ID {account_id} not found"
                    )
                
                previous_balance = float(account.balance)
                amount = debit_request.amount
                
                if previous_balance < amount:
                    # Create failed transaction record
                    transaction = Transaction(
                        id=transaction_id,
                        account_id=account_id,
                        transaction_type="debit",
                        amount=amount,
                        status="failed",
                        reference=debit_request.reference,
                        description=debit_request.description
                    )
                    db.add(transaction)
                    db.commit()
                    
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "error": "insufficient_funds",
                            "message": "Insufficient funds for this transaction",
                            "details": f"Current balance: {previous_balance}, Requested debit: {amount}"
                        }
                    )
                
                # Update account balance
                new_balance = previous_balance - amount
                account.balance = new_balance
                
                # Create transaction record
                transaction = Transaction(
                    id=transaction_id,
                    account_id=account_id,
                    transaction_type="debit",
                    amount=amount,
                    status="completed",
                    reference=debit_request.reference,
                    description=debit_request.description
                )
                db.add(transaction)
                
                # Commit the transaction
                db.commit()
                
                # Return response
                return {
                    "transaction_id": transaction_id,
                    "account_id": account_id,
                    "type": "debit",
                    "amount": amount,
                    "previous_balance": previous_balance,
                    "new_balance": new_balance,
                    "reference": debit_request.reference,
                    "timestamp": transaction.timestamp,
                    "status": "completed"
                }
                
            except Exception as e:
                db.rollback()
                logger.error(f"Transaction failed: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "error": "transaction_failed",
                        "message": "Failed to process transaction",
                        "details": str(e)
                    }
                )
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions
        raise http_ex
    except Exception as e:
        # Handle any other exceptions that might occur
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
                "details": str(e)
            }
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=8000)