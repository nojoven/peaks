from fastapi import APIRouter, HTTPException, Depends, Response, Query, Request
from sqlmodel import Session, select
from src.models.peak import Peak
from src.core.database import get_db
from src.api.authentication import require_login
from typing import List
from fastapi.responses import RedirectResponse

# Create a router for the peaks endpoints
router = APIRouter()


@router.get("/peaks/peak/{peak_id}", response_model=Peak)
@require_login
async def read_peak(peak_id: int, db: Session = Depends(get_db)):
    peak = db.exec(select(Peak).where(Peak.id == peak_id)).first()
    if peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return peak


@router.post("/peaks/peak/create", response_model=Peak, status_code=201)
@require_login
async def create_peak(peak: Peak, db: Session = Depends(get_db)):
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

@router.post("/peaks/create", response_model=List[Peak], status_code=201)
@require_login
async def bulk_create_peaks(peaks: List[Peak], db: Session = Depends(get_db)):
    """Bulk create peaks from a list."""
    try:
        db.add_all(peaks)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error bulk creating of peaks: {str(e)}"
        ) from e
    
    return Response(status_code=201, content="Peaks were inserted successfully")
    

@router.put("/peaks/peak/{peak_id}", response_model=Peak)
@require_login
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
    return Response(status_code=200)


@router.delete("/peaks/peak/{peak_id}")
@require_login
async def delete_peak(peak_id: int, db: Session = Depends(get_db)):
    db_peak = db.exec(select(Peak).where(Peak.id == peak_id)).first()
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    
    db.delete(db_peak)
    db.commit()
    return Response(status_code=204)


@router.get("/peaks/boundingbox", response_model=List[Peak])
@require_login
async def get_peaks_in_bounding_box(
    min_lat: float = Query(..., description="Minimum latitude"),
    max_lat: float = Query(..., description="Maximum latitude"),
    min_lon: float = Query(..., description="Minimum longitude"),
    max_lon: float = Query(..., description="Maximum longitude"),
    db: Session = Depends(get_db)
):
    """
    Retrieve peaks within a given geographical bounding box.
    """
    statement = select(Peak).where(
        Peak.lat >= min_lat,
        Peak.lat <= max_lat,
        Peak.lon >= min_lon,
        Peak.lon <= max_lon
    )
    results = db.exec(statement)
    peaks = results.all()
    if not len(peaks):
        raise HTTPException(status_code=404, detail="No peaks found in the bounding box")
    return peaks

# Retrieve all peaks
@router.get("/peaks", response_model=List[Peak])
@require_login
async def fetch_peaks(request: Request, db: Session = Depends(get_db)):
    """
    Fetch all peaks and return them in a list of dictionaries.
    """
    return db.exec(select(Peak)).all()