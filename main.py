from fastapi import FastAPI
from pydantic import BaseModel
import requests

# Initialize the FastAPI app
app = FastAPI()

# Create a Pydantic model for request data
class ConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

# API endpoint to fetch exchange rates from an external API
def fetch_exchange_rates(base_currency: str):
    # You can use any public exchange rate API here.
    # For this example, let's use ExchangeRate API.
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if 'rates' in data:
        return data['rates']
    else:
        return {}

# API endpoint for currency conversion
@app.post("/convert/")
async def convert_currency(request: ConversionRequest):
    # Fetch exchange rates for the from_currency
    rates = fetch_exchange_rates(request.from_currency)

    # Check if the currency pair is valid
    if request.to_currency not in rates:
        return {"error": "Invalid currency pair"}

    # Calculate the converted amount
    conversion_rate = rates[request.to_currency]
    converted_amount = request.amount * conversion_rate

    # Return the result
    return {
        "from_currency": request.from_currency,
        "to_currency": request.to_currency,
        "original_amount": request.amount,
        "converted_amount": converted_amount,
        "conversion_rate": conversion_rate,
    }

# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Currency Converter API is running!"}


# Define the request parameters as a Pydantic model
class ConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

# Define the GET endpoint
@app.get("/get_conversion_data/")
async def get_conversion_data():
    # You can return the JSON directly
    return {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    }