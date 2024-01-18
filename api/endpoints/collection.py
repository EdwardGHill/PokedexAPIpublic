from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import get_db
from api.endpoints.auth import get_current_user
from api.models import Collection, User, Pokemon
from api.schemas.collection import CollectionCreate, CollectionResponse
from typing import List


router = APIRouter()

@router.post("/", response_model=CollectionResponse)
def add_to_collection(collection: CollectionCreate, current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            existing_collection = session.query(Collection).filter_by(pokemon_id=collection.pokemon_id, user_id=current_user.id).first()
            if existing_collection:
                raise HTTPException(status_code=400, detail="This pokemon is already in Collection")

            pokemon = session.query(Pokemon).get(collection.pokemon_id)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")

            db_collection = Collection(pokemon_id=collection.pokemon_id, user_id=current_user.id)
            session.add(db_collection)
            session.commit()
            session.refresh(db_collection)

        return {"id": db_collection.id, "pokemon_id": db_collection.pokemon_id}
    finally:
        db.__exit__(None, None, None)

@router.get("/", response_model=List[CollectionResponse])
def get_collection(current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            collection = session.query(Collection).filter_by(user_id=current_user.id).all()

        collection_response = [
            {"id": collection.id, "pokemon_id": collection.pokemon_id}
            for collection in collection
        ]
        return collection_response
    finally:
        db.__exit__(None, None, None)


@router.delete("/{pokemon_id}", status_code=204)
def delete_collection(pokemon_id: int, current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            collection = session.query(Collection).filter_by(pokemon_id=pokemon_id, user_id=current_user.id).first()
            if not collection:
                raise HTTPException(status_code=404, detail="Collection not found")
            session.delete(collection)
            session.commit()
    finally:
        db.__exit__(None, None, None)