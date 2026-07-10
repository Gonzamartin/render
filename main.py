import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Meteorologica AgTech Directa")

# Permitir conexiones desde tu aplicacion de C# sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def obtener_clima_directo(lat: float = -34.12, lon: float = -60.57):
    """
    Procesa el clima directamente en la raiz del servidor.
    Si C# no envia datos, usa las coordenadas por defecto del lote.
    """
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            datos = response.json()
            clima_actual = datos["current_weather"]
            temp = float(clima_actual["temperature"])
            viento = float(clima_actual["windspeed"])
            
            # Criterio agronomico estandar para la aplicacion
            apto = "APTO" if (5 <= viento <= 15 and temp < 30) else "NO APTO"
            
            return {
                "temperatura_celsius": temp,
                "viento_kmh": viento,
                "pulverizacion": apto
            }
        else:
            return {
                "temperatura_celsius": 0.0,
                "viento_kmh": 0.0,
                "pulverizacion": f"Error OpenMeteo {response.status_code}"
            }
            
    except Exception as e:
        return {
            "temperatura_celsius": 0.0,
            "viento_kmh": 0.0,
            "pulverizacion": "Falla de red en nube"
        }
