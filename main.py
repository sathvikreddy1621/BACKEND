from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read API keys from .env (secure)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
COINSWITCH_API_KEY = os.getenv("COINSWITCH_API_KEY")

USD_TO_INR = 83  # Fixed conversion rate (acceptable for projects)

# ---------------- BINANCE (USD → INR) ----------------
@app.get("/price/binance")
def binance_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BTCUSDT"}
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    r = requests.get(url, params=params, headers=headers).json()
    inr_price = round(float(r["price"]) * USD_TO_INR, 2)

    return {
        "platform": "Binance",
        "currency": "INR",
        "price": inr_price
    }

# ---------------- COINBASE (USD → INR) ----------------
@app.get("/price/coinbase")
def coinbase_price():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    headers = {"Authorization": f"Bearer {COINBASE_API_KEY}"}

    r = requests.get(url, headers=headers).json()
    inr_price = round(float(r["data"]["amount"]) * USD_TO_INR, 2)

    return {
        "platform": "Coinbase",
        "currency": "INR",
        "price": inr_price
    }

# ---------------- COINGECKO (DIRECT INR) ----------------
@app.get("/price/coingecko")
def coingecko_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "inr"}

    r = requests.get(url, params=params).json()

    return {
        "platform": "CoinGecko",
        "currency": "INR",
        "price": r["bitcoin"]["inr"]
    }

# ---------------- COINSWITCH (INR – DERIVED) ----------------
@app.get("/price/coinswitch")
def coinswitch_price():
    """
    CoinSwitch does not expose public ticker prices.
    INR price derived from trusted market data.
    """

    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "inr"}
    ).json()

    return {
        "platform": "CoinSwitch",
        "currency": "INR",
        "price": r["bitcoin"]["inr"]
    }
