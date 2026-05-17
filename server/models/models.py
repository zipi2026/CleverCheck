"""
models/models.py — הגדרת טבלאות SQLAlchemy
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, Float, String, Boolean,
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GradingResult(Base):
    """תוצאת הערכה כוללת לבקשת ציון אחת."""
    __tablename__ = 'GradingResult'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    submission_id       = Column(Integer, nullable=False, index=True)
    final_score         = Column(Float,   nullable=False)
    confidence          = Column(String(10), nullable=False)   # 'high' / 'low'
    needs_llm_review    = Column(Boolean, nullable=False, default=False)
    needs_human_review  = Column(Boolean, nullable=False, default=False)
    graded_at           = Column(DateTime, default=datetime.utcnow)

    concepts = relationship(
        'ConceptEvaluation',
        back_populates='grading_result',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (
            f"<GradingResult id={self.id} "
            f"submission={self.submission_id} "
            f"score={self.final_score:.2f}>"
        )


class ConceptEvaluation(Base):
    """פירוט הערכה לכל מושג מפתח בנפרד (One-to-Many → GradingResult)."""
    __tablename__ = 'ConceptEvaluation'

    id                = Column(Integer, primary_key=True, autoincrement=True)
    grading_result_id = Column(Integer, ForeignKey('GradingResult.id'), nullable=False)
    concept           = Column(String(200), nullable=False)
    similarity        = Column(Float,       nullable=False)
    best_segment      = Column(Text,        nullable=True)
    negation_detected = Column(Boolean,     nullable=False, default=False)
    status            = Column(String(20),  nullable=False)   # correct/negated/missing

    grading_result = relationship('GradingResult', back_populates='concepts')

    def __repr__(self):
        return f"<ConceptEvaluation concept='{self.concept}' status='{self.status}'>"
