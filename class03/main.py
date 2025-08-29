from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import requests

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    tracing_disabled= True
)

@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Get current price of cryptocurrency (e.g. BTCUSDT, ETHUSDT).
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        response.raise_for_status()
        price = response.json()["price"]
        return f"The current price of {symbol.upper()} is **${price}**."
    except Exception as e:
        return f"Failed to fetch price for {symbol.upper()}. Error: {e}"
    


crypto_agent = Agent(
    name="CryptoDataAgent",
    instructions="You provide real-time crypto prices using the Binance API.",
    tools=[get_crypto_price]
)

async def main():

    response = await  Runner.run(
        crypto_agent,
        input = 'tell me BTCUSDT rate of Bitcoin ',
        run_config = config
        )
    print(response)

if __name__ == '__main__':
    asyncio.run(main())