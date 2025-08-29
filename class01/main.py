from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

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


async def main():
    translator_agent = Agent(
        name = 'Translator Agent',
        instructions = 'Your task is to translate the text that the user give you in English',
    )

    response = await  Runner.run(
        translator_agent,
        input = 'Translate : mai umer hun , mujhy acha lagta hai mobile chalana khelna kuudna baatain karna hasi mazaak karna shahi khana khana ',
        run_config = config
        )
    print(response)

if __name__ == '__main__':
    asyncio.run(main())