from fastapi import FastAPI
import uvicorn


def main():
    print("Hello from uv-use-latest!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from uv-use-latest!"}

if __name__ == "__main__":
    main()
