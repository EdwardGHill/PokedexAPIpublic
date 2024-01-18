from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    pokemon_id: int
    # user_id: int

class FavoriteResponse(BaseModel):
    id: int
    pokemon_id: int
