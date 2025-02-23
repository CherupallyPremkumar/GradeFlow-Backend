from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)  # URL/path to the profile image
    job_title = Column(String, nullable=False)  # e.g., "Software Developer"
    location = Column(String, nullable=False)  # e.g., "San Francisco, CA"
    about_me = Column(Text, nullable=False)  # Overview/bio of the user
    skills = Column(Text, nullable=False)  # Comma-separated skills (e.g., "JavaScript, React, Node.js")
    experience = Column(Text, nullable=False)  # JSON/serialized string of experience list
    education_overview = Column(Text, nullable=False)  # JSON/serialized string of education details

    def __repr__(self):
        return f"<User(username={self.username}, job_title={self.job_title})>"