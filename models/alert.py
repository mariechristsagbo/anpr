from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class AlertType(enum.Enum):
    STOLEN_VEHICLE = "stolen_vehicle"
    SUSPICIOUS_VEHICLE = "suspicious_vehicle"
    CAMERA_OFFLINE = "camera_offline"
    DETECTION_ERROR = "detection_error"
    SYSTEM_ERROR = "system_error"
    LOW_CONFIDENCE = "low_confidence"

class AlertSeverity(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(enum.Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.MEDIUM, nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.NEW, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)  # Additional alert information
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Foreign Keys
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    detection = relationship("Detection", back_populates="alerts")
    vehicle = relationship("Vehicle")
    camera = relationship("Camera")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="alerts_created")
    acknowledged_by = relationship("User", foreign_keys=[acknowledged_by_id], back_populates="alerts_acknowledged")
    resolved_by = relationship("User", foreign_keys=[resolved_by_id], back_populates="alerts_resolved")

    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.type.value}', status='{self.status.value}')>" 