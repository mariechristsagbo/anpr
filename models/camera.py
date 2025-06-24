from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    camera_type = Column(String, default="fixed", nullable=False)  # fixed, mobile, ptz
    status = Column(String, default="offline", nullable=False)  # online, offline, error, maintenance
    stream_url = Column(String, nullable=True)
    rtsp_url = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    camera_settings = Column(JSON, nullable=True)  # Resolution, FPS, etc.
    last_ping = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    detections = relationship("Detection", back_populates="camera")

    def __repr__(self):
        return f"<Camera(id={self.id}, name='{self.name}', status='{self.status}')>" 