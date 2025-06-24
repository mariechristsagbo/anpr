from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=True)  # car, truck, motorcycle, etc.
    year = Column(Integer, nullable=True)
    country = Column(String, default="BENIN", nullable=False)
    is_stolen = Column(Boolean, default=False, nullable=False)
    stolen_reported_at = Column(DateTime(timezone=True), nullable=True)
    stolen_reported_by = Column(Integer, nullable=True)  # User ID
    vehicle_metadata = Column(JSON, nullable=True)  # Additional vehicle info
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    detections = relationship("Detection", back_populates="vehicle")
    stolen_vehicle_record = relationship("StolenVehicle", back_populates="vehicle", uselist=False)

    def __repr__(self):
        return f"<Vehicle(id={self.id}, plate='{self.plate_number}', is_stolen={self.is_stolen})>" 