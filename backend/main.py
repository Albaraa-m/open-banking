from pathlib import Path
from typing import List

from database import get_db
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import User
from schemas.user import UserCreate, UserSchema
from sqlalchemy.orm import Session
from utils.lean_client import LeanClient

parent_dir = Path(__file__).parent.parent
env_path = parent_dir / ".env"
load_dotenv(env_path)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user/", response_model=UserSchema)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user_data.name).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this name already exists"
        )

    try:
        lean_client = LeanClient()
        customer_id = await lean_client.create_customer(user_data.name)
        user = User(name=user_data.name, customer_id=customer_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except HTTPException as e:
        raise e


@app.get("/user/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/token/{customer_id}")
async def get_customer_token(customer_id: str):
    lean_client = LeanClient()
    return await lean_client.generate_access_token(customer_id)
