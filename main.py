import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Auditoría AgTech",
    description="Servidor en la nube para evadir bloqueos locales y procesar datos climáticos."
)

# Permitir que tu aplicación de C# se conecte desde cualquier computadora sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {"status": "Servidor AgTech en línea", "mensaje": "Listo para auditar lotes."}

@app.get("/clima")
def obtener_clima_lote(lat: float, lon: float):
    """
    Este endpoint será llamado por C#. Al ejecutarse en la nube, 
    Open-Meteo responderá instantáneamente sin bloqueos de ISP corporativos.
    """
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    
    try:
        # La nube tiene internet libre, por lo que esta petición estándar funcionará siempre
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            datos = response.json()
            clima_actual = datos["current_weather"]
            temp = clima_actual["temperature"]
            viento = clima_actual["windspeed"]
            
            # Lógica agronómica básica para el reporte técnico
            apto_pulverizar = "APTO" if (5 <= viento <= 15 and temp < 30) else "NO APTO (Revisar deriva/inversión)"
            
            return {
                "coordenadas": {"latitud": lat, "longitud": lon},
                "temperatura_celsius": temp,
                "viento_kmh": viento,
                "pulverizacion": apto_pulverizar
            }
        else:
            raise HTTPException(status_code=500, detail="Error al consultar el proveedor meteorológico internacional.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falla de red en el servidor en la nube: {str(e)}")
