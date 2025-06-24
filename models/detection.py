from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    detection_confidence = Column(Float, nullable=True)  # YOLO confidence
    recognition_confidence = Column(Float, nullable=True)  # OCR confidence
    ocr_text = Column(String, nullable=True)
    bounding_box = Column(JSON, nullable=True)  # {x, y, width, height}
    recognition_polygon = Column(JSON, nullable=True)  # OCR polygon coordinates
    image_path = Column(String, nullable=True)  # Path to stored image
    image_data = Column(Text, nullable=True)  # Base64 encoded image
    processing_time = Column(Float, nullable=True)  # Processing time in ms
    vehicle_type = Column(String, nullable=True)
    vehicle_color = Column(String, nullable=True)
    vehicle_brand = Column(String, nullable=True)
    vehicle_model = Column(String, nullable=True)
    detection_metadata = Column(JSON, nullable=True)  # Additional detection info
    is_alert_triggered = Column(Boolean, default=False, nullable=False)
    
    # Foreign Keys
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    vehicle = relationship("Vehicle", back_populates="detections")
    camera = relationship("Camera", back_populates="detections")
    created_by = relationship("User", back_populates="detections")
    alerts = relationship("Alert", back_populates="detection")

    def __repr__(self):
        return f"<Detection(id={self.id}, plate='{self.plate_number}', confidence={self.confidence:.2f})>" 