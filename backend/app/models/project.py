from sqlalchemy import Column, String, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Project(Base):
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    target_amount = Column(Numeric(10, 2))
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    contributions = relationship("Contribution", back_populates="project") 