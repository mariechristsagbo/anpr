from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class StolenVehicle(Base):
    __tablename__ = "stolen_vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, nullable=False, index=True)
    report_number = Column(String, unique=True, nullable=False)  # Police report number
    stolen_date = Column(DateTime(timezone=True), nullable=False)
    stolen_location = Column(String, nullable=True)
    stolen_location_lat = Column(Float, nullable=True)
    stolen_location_lng = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    police_station = Column(String, nullable=True)
    contact_person = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)  # Still being searched
    recovered_date = Column(DateTime(timezone=True), nullable=True)
    recovered_location = Column(String, nullable=True)
    recovery_notes = Column(Text, nullable=True)
    stolen_vehicle_metadata = Column(JSON, nullable=True)  # Additional stolen vehicle info
    
    # Foreign Keys
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recovered_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    vehicle = relationship("Vehicle", back_populates="stolen_vehicle_record")
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    recovered_by = relationship("User", foreign_keys=[recovered_by_id])

    def __repr__(self):
        return f"<StolenVehicle(id={self.id}, plate='{self.plate_number}', is_active={self.is_active})>" 