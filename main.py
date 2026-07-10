import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Auditoría AgTech")

# Permitir conexiones de C# sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {"status": "Servidor AgTech en línea"}

@app.get("/clima")
def obtener_clima_lote(lat: float, lon: float):
    # URL estándar de Open-Meteo
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    
    # Camuflaje obligatorio para que Open-Meteo no bloquee a tu servidor de Render
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            datos = response.json()
            clima_actual = datos["current_weather"]
            temp = float(clima_actual["temperature"])
            viento = float(clima_actual["windspeed"])
            
            # Lógica agronómica para la ventana de trabajo
            apto = "APTO" if (5 <= viento <= 15 and temp < 30) else "NO APTO"
            
            return {
                "temperatura_celsius": temp,
                "viento_kmh": viento,
                "pulverizacion": apto
            }
        else:
            # Si Open-Meteo falla, devolvemos un JSON limpio, NO un HTML de error
            return {
                "temperatura_celsius": 0.0,
                "viento_kmh": 0.0,
                "pulverizacion": f"Error proveedor (Código {response.status_code})"
            }
            
    except Exception as e:
        return {
            "temperatura_celsius": 0.0,
            "viento_kmh": 0.0,
            "pulverizacion": "Error de conexión en nube"
        }
