from src.web.server import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, reload=True) 