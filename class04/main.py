from agents import Agent, Runner, function_tool
from connection import config
from datetime import datetime
import requests


@function_tool
def get_products():
    """ 
     fetches a list of products from template six
    """
    url = 'https://template6-six.vercel.app/api/products'
    try:
        response = requests.get(url)
        data = response.json()

        return[
            {
                "title":p.get("title"),
                "price":p.get("price"),
                "description":p.get("description")
            }
            for p in data
        ]
    except Exception as e:
        return {"error": str(e)}

agent=Agent(
    name="Shopping Agent",
    instructions="you are a helpful shopping assistant . Use the product list from the API to recommend products based on user's query",
    tools=[get_products]
)

shopping_queries = [
    "Show me all available products from the store",
    "What are the newest products available",
    "Which items are great as a birthday gift?"
]

a = int(input("enter the index to get that query : " ))
 
b = shopping_queries[a]

result = Runner.run_sync(
    agent,
    b,
    run_config=config
)

print(result.final_output)