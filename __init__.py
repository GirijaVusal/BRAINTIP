import uvicorn
from utils import load_config

config = load_config()

if __name__ == "__main__":
    workers = config["settings"]["workers"]
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=workers)
