from fastapi import APIRouter, HTTPException, Depends, Response
from sqlmodel import Session, select
from src.models.peak import Peak
from src.core.database import get_db

# Create a router for the peaks endpoints
router = APIRouter()


@router.get("/peaks/peak/{peak_id}", response_model=Peak)
async def read_peak(peak_id: int, db: Session = Depends(get_db)):
    peak = db.exec(select(Peak).where(Peak.id == peak_id)).first()
    if peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return peak


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


@router.put("/peaks/peak/{peak_id}", response_model=Peak)
async def update_peak(peak_id: int, peak: Peak, db: Session = Depends(get_db)):
    db_peak = db.exec(select(Peak).where(Peak.id == peak_id)).first()
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    
    # Update the Peak fields
    db_peak.name = peak.name
    db_peak.lat = peak.lat
    db_peak.lon = peak.lon
    db_peak.altitude = peak.altitude
    db.commit()
    db.refresh(db_peak)
    return Response(status_code=204)