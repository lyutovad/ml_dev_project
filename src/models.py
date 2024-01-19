from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Integer,
    String,
    Column,
    DateTime,
    ForeignKey,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
NAME = os.getenv("POSTGRES_DB")


Base = declarative_base()

metadata = MetaData()
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}")

# sess = sessionmaker(bind=engine)
# session = Session(sess)
session = Session(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, index=True)
    password = Column(String(250), nullable=False)
    email = Column(String(25), nullable=False)
    name = Column(String(20))
    surname = Column(String(20))
    created_on = Column(DateTime())
    updated_on = Column(DateTime())
    user_models = relationship("UserModel")
    credits = relationship("Credit")


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    user_models = relationship("UserModel")


class Prediction(Base):
    __tablename__ = "data_prediction"
    id = Column(Integer, primary_key=True)
    prediction = Column(Integer)
    Years_at_diagnosis = Column(Integer, nullable=False)
    Days_at_diagnosis = Column(Integer, nullable=False)
    Race = Column(String(20), nullable=False)
    IDH1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    TP53 = Column(String(11), nullable=False, default="NOT_MUTATED")
    ATRX = Column(String(11), nullable=False, default="NOT_MUTATED")
    PTEN = Column(String(11), nullable=False, default="NOT_MUTATED")
    EGFR = Column(String(11), nullable=False, default="NOT_MUTATED")
    CIC = Column(String(11), nullable=False, default="NOT_MUTATED")
    MUC16 = Column(String(11), nullable=False, default="NOT_MUTATED")
    PIK3CA = Column(String(11), nullable=False, default="NOT_MUTATED")
    NF1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    PIK3R1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    FUBP1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    RB1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    NOTCH1 = Column(String(11), nullable=False, default="NOT_MUTATED")
    BCOR = Column(String(11), nullable=False, default="NOT_MUTATED")
    CSMD3 = Column(String(11), nullable=False, default="NOT_MUTATED")
    SMARCA4 = Column(String(11), nullable=False, default="NOT_MUTATED")
    GRIN2A = Column(String(11), nullable=False, default="NOT_MUTATED")
    IDH2 = Column(String(11), nullable=False, default="NOT_MUTATED")
    FAT4 = Column(String(11), nullable=False, default="NOT_MUTATED")
    PDGFRA = Column(String(11), nullable=False, default="NOT_MUTATED")
    result = Column(Integer())
    model = Column(ARRAY(Integer))
    user_models = relationship("UserModel")


class UserModel(Base):
    __tablename__ = "user_models"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    model_id = Column(ForeignKey("models.id"))
    data_id = Column(ForeignKey("data_prediction.id"))
    used_on = Column(DateTime())
    uid = Column(UUID(as_uuid=True), nullable=False)


class Credit(Base):
    __tablename__ = "credits"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    operation_type_id = Column(ForeignKey("operation_type.id"))
    amount = Column(Integer(), nullable=False)
    uid = Column(UUID(as_uuid=True))


class Operation(Base):
    __tablename__ = "operation_type"
    id = Column(Integer, primary_key=True)
    type = Column(String(5), nullable=False)
    credits = relationship("Credit")


# Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
