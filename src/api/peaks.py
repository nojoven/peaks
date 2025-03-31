from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from src.models.peak import Peak
from src.core.database import get_db

# Create a router for the peaks endpoints
router = APIRouter()

@router.post("/peaks/peak/create", response_model=Peak, status_code=201)
def create_peak(peak: Peak, db: Session = Depends(get_db)):
    """Create a new peak in the database."""
    try:
        # Add the peak to the session
        db.add(peak)
        db.commit()  # Commit the transaction
        db.refresh(peak)  # Refresh to get the generated ID
        return peak  # Return the created peak
    except Exception as e:
        # If an error occurs, raise an HTTPException
        db.rollback()  # Rollback the transaction to keep the session clean
        raise HTTPException(
            status_code=400, detail=f"Error creating peak: {str(e)}"
        ) from e