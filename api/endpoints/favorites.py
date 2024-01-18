from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import get_db
from api.endpoints.auth import get_current_user
from api.models import Favorite, User, Pokemon
from api.schemas.favorites import FavoriteCreate, FavoriteResponse
from typing import List


router = APIRouter()

@router.post("/", response_model=FavoriteResponse)
def add_to_favorites(favorite: FavoriteCreate, current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            existing_favorite = session.query(Favorite).filter_by(pokemon_id=favorite.pokemon_id, user_id=current_user.id).first()
            if existing_favorite:
                raise HTTPException(status_code=400, detail="This pokemon is already in Favorites")

            pokemon = session.query(Pokemon).get(favorite.pokemon_id)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokemon not found")

            db_favorite = Favorite(pokemon_id=favorite.pokemon_id, user_id=current_user.id)
            session.add(db_favorite)
            session.commit()
            session.refresh(db_favorite)

        return {"id": db_favorite.id, "pokemon_id": db_favorite.pokemon_id}
    finally:
        db.__exit__(None, None, None)

@router.get("/", response_model=List[FavoriteResponse])
def get_favorites(current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            favorites = session.query(Favorite).filter_by(user_id=current_user.id).all()

        favorites_response = [
            {"id": favorite.id, "pokemon_id": favorite.pokemon_id}
            for favorite in favorites
        ]
        return favorites_response
    finally:
        db.__exit__(None, None, None)


@router.delete("/{pokemon_id}", status_code=204)
def delete_favorite(pokemon_id: int, current_user: User = Depends(get_current_user)):
    db = get_db()
    try:
        with db as session:
            favorite = session.query(Favorite).filter_by(pokemon_id=pokemon_id, user_id=current_user.id).first()
            if not favorite:
                raise HTTPException(status_code=404, detail="Favorite not found")
            session.delete(favorite)
            session.commit()
    finally:
        db.__exit__(None, None, None)