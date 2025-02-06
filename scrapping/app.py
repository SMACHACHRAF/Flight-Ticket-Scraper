from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

# Charger les données CSV au démarrage
file_path = "flight_offers.csv"
try:
    flights_data = pd.read_csv(file_path)
    flights_data.columns = [col.lower().replace(" ", "_") for col in flights_data.columns]  # Normaliser les noms de colonnes
except Exception as e:
    flights_data = None
    print(f"Erreur lors du chargement du fichier CSV : {e}")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des vols !"}

# Endpoint pour lister tous les vols
@app.get("/flights")
def get_flights():
    if flights_data is None:
        raise HTTPException(status_code=500, detail="Données des vols non disponibles.")
    return flights_data.to_dict(orient="records")

# Endpoint pour rechercher un vol par destination
@app.get("/flights/search/{destination}")
def search_flight(destination: str):
    if flights_data is None:
        raise HTTPException(status_code=500, detail="Données des vols non disponibles.")
    results = flights_data[flights_data["arrival"].str.contains(destination, case=False, na=False)]
    if results.empty:
        raise HTTPException(status_code=404, detail="Aucun vol trouvé pour cette destination.")
    return results.to_dict(orient="records")

# Endpoint pour filtrer les vols par prix
@app.get("/flights/filter")
def filter_flights(min_price: float = 0, max_price: float = float("inf")):
    if flights_data is None:
        raise HTTPException(status_code=500, detail="Données des vols non disponibles.")
    results = flights_data[(flights_data["price"] >= min_price) & (flights_data["price"] <= max_price)]
    if results.empty:
        raise HTTPException(status_code=404, detail="Aucun vol trouvé dans cette plage de prix.")
    return results.to_dict(orient="records")

# Endpoint pour trier les vols
@app.get("/flights/sort")
def sort_flights(order: str = "asc", sort_by: str = Query("price", regex="^(price|departure_date)$")):
    if flights_data is None:
        raise HTTPException(status_code=500, detail="Données des vols non disponibles.")
    ascending = True if order == "asc" else False
    try:
        results = flights_data.sort_values(by=sort_by, ascending=ascending)
        return results.to_dict(orient="records")
    except KeyError:
        raise HTTPException(status_code=400, detail="Critère de tri invalide.")
