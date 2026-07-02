from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Device
from app.schemas import DeviceCreate, DeviceResponse

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
) -> Device:
    device = Device(
        id=str(uuid4()),
        name=device_data.name,
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device

@router.get(
    "",
    response_model=list[DeviceResponse],
)
def list_devices(db: Session = Depends(get_db),) -> list[Device]:
    statement = select(Device).order_by(Device.created_at, Device.id)
    devices = list(db.scalars(statement).all())

    return devices
