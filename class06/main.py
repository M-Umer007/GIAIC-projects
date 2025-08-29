from agents import Agent, Runner, trace
from connection import config
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv

load_dotenv()


lyric_analyst = Agent(
    name="Lyric Agent",
    instructions="""
        You analyze the lyrical qualities of a poem.
        Focus on rhyme, rhythm, word choice, sound patterns,
        and overall musicality of the text.
    """,
)

narrative_analyst_agent = Agent(
    name="Narrative Analyst Agent",
    instructions="""
        You analyze the narrative aspects of a poem.
        Focus on storytelling elements such as characters, 
        plot, setting, tone, and how the poem conveys a journey or event.
    """,
)

dynamic_analyst_agent = Agent(
    name="Dynamic Analyst Agent",
    instructions="""
        You analyze the emotional and thematic dynamics of a poem.
        Focus on shifts in mood, intensity, symbolism, themes, 
        and the overall emotional progression.
    """,
)


poet_agent = Agent(
    name="Poet Agent",
    instructions="""
        You are a Poet Agent. Your role is to take an input poem 
        and decide which specialized analyst should process it next 
        (lyric, narrative, or dynamic).
    """,
    handoffs=[lyric_analyst, narrative_analyst_agent, dynamic_analyst_agent],
)


async def main():
    while True:
        msg = input("Enter your message : " )

        with trace("Class 06"):

            result = await Runner.run(poet_agent, msg, run_config=config)
            print(result.last_agent.name)
            print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())