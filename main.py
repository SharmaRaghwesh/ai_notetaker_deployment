from main_api import app

# This allows Railway (or anyone running main.py) to serve the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=False)