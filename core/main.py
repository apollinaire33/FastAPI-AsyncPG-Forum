from fastapi import FastAPI, status

app = FastAPI()

@app.get('/')
def create():
    return 'shosho'
