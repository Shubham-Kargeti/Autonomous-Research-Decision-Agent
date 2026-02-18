import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base


# ==========================================================
# USER MODEL (Auth0 Based)
# ==========================================================
class User(Base):
    __tablename__ = "users"

    # Internal primary key (used by our system)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Auth0 unique identifier (VERY IMPORTANT)
    # Example: "auth0|67c9abc123..."
    auth0_sub = Column(String, unique=True, index=True, nullable=False)

    # Optional profile info from Auth0 token
    email = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with AgentRun
    runs = relationship("AgentRun", back_populates="user", cascade="all, delete")


# ==========================================================
# AGENT RUN HISTORY
# ==========================================================
class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    goal = Column(Text, nullable=False)
    plan = Column(JSONB)
    result = Column(JSONB)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="runs")
