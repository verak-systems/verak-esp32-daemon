from fastapi import FastAPI, Response, status
import sqlite3

app = FastAPI()

con = sqlite3.connect("database/sensor_data.db3")
cur = con.cursor()

@app.get("/get_all_temps/analog")
async def read_all_analog(response: Response):
    try:
        cur.execute('SELECT * FROM analogTemp')
        data = cur.fetchall()

        response.status_code = status.HTTP_200_OK
        return {"data": data}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": e}

@app.get("/get_all_temps/digital")
async def read_all_digital(response: Response):
    try:
        cur.execute('SELECT * FROM digitalTemp')
        data = cur.fetchall()

        response.status_code = status.HTTP_200_OK
        return {"data": data}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": e}

@app.get("/get_devices/all")
async def read_all_devices(response: Response):
    try:
        cur.execute('SELECT * FROM device')
        data = cur.fetchall()

        response.status_code = status.HTTP_200_OK
        return {"data": data}
    
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": e}
    
    