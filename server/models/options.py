from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Option(Base):
    """אפשרות תשובה לשאלה סגורה (Multiple Choice)."""

    __tablename__ = "Options"

    # =========================
    # PK
    # =========================
    id = Column("OptionID", Integer, primary_key=True, autoincrement=True)

    # =========================
    # FIELDS
    # =========================
    option_number = Column("OptionNumber", Integer, nullable=False)

    question_id = Column(
        "QuestionID",
        Integer,
        ForeignKey("Questions.QuestionID", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    option_text = Column("OptionText", Text, nullable=False)

    # =========================
    # CONSTRAINTS
    # =========================
    __table_args__ = (
        UniqueConstraint(
            "QuestionID",
            "OptionNumber",
            name="UQ_Question_OptionNumber"
        ),
    )

    # =========================
    # RELATIONSHIPS
    # =========================
    question = relationship("Question", back_populates="options")

    # =========================
    # DEBUG
    # =========================
    def __repr__(self):
        return (
            f"<Option id={self.id} "
            f"question_id={self.question_id} "
            f"number={self.option_number}>"
        )