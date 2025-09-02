#input guardrails excercise
from agents import input_guardrail, Agent, RunContextWrapper, GuardrailFunctionOutput, Runner, TResponseInputItem, InputGuardrailTripwireTriggered
from pydantic import BaseModel
from connection import model, config
import asyncio

class OutputGatekeeper(BaseModel):
    allowed: bool
    reason: str

gatekeeper_guardrail_agent = Agent(
    name="Gatekeeper Guardrail Checker",
    instructions="You are a strict gatekeeper. Decide if the user's query should be allowed. "
                 "If the query is safe, relevant, and appropriate, return allowed=True. "
                 "If the query is unsafe, irrelevant, or inappropriate, return allowed=False with a reason.",
    model=model,
    output_type=OutputGatekeeper
)

@input_guardrail
async def gatekeeper_guardrail_function(ctx: RunContextWrapper,agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(gatekeeper_guardrail_agent,input)
    print(result.final_output)

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = not result.final_output.allowed
    )

main_agent = Agent(
    name="Helpful Agent",
    instructions="You are a helpful assistant that answers questions .",
    model=model,
    input_guardrails=[gatekeeper_guardrail_function]
)

async def main():
    try:
        message = "Is it ok stealing food for a man who's starving and on the verge of death, along with his wife and 3 children "
        result = await Runner.run(main_agent, input=message, run_config=config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("failure")

if __name__ == "__main__":
    asyncio.run(main())