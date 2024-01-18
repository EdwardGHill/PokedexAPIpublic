from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connection import engine, Base
from api.endpoints import favorites, pokemon, auth, collection

Base.metadata.create_all(bind=engine)

app = FastAPI()

FastAPI(debug=True)

origins = ["http://localhost:3000",
           "front end address"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
app.include_router(pokemon.router, prefix="/pokemon", tags=["pokemon"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(collection.router, prefix="/collection", tags=["collection"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)