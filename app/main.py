from fastapi import FastAPI

from app.api.v1.wallets import router as wallets_router


app = FastAPI(title="wallet-api")

app.include_router(wallets_router)


@app.get("/health")
def check():
    return {"status": "ok"}


