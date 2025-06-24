from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    detections = relationship("Detection", back_populates="created_by", foreign_keys="Detection.created_by_id")
    alerts_created = relationship("Alert", back_populates="created_by", foreign_keys="Alert.created_by_id")
    alerts_acknowledged = relationship("Alert", foreign_keys="Alert.acknowledged_by_id")
    alerts_resolved = relationship("Alert", foreign_keys="Alert.resolved_by_id")
    stolen_vehicles_reported = relationship("StolenVehicle", foreign_keys="StolenVehicle.reported_by_id")
    stolen_vehicles_recovered = relationship("StolenVehicle", foreign_keys="StolenVehicle.recovered_by_id")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>" 