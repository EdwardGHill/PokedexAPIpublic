from pydantic import BaseModel

class CollectionCreate(BaseModel):
    pokemon_id: int
    # user_id: int

class CollectionResponse(BaseModel):
    id: int
    pokemon_id: int