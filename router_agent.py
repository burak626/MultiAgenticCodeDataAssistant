from python_agent import python_executor
from csv_agent import csv_executor
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage



# Router agent for directing requests to appropriate specialized agents

def python_agent_wrapper(input_text):
    return python_executor.invoke({"input": input_text})

def csv_agent_wrapper(input_text):
    from csv_agent import csv_executor
    if csv_executor is None:
        return {"output": "Please upload a CSV file first before asking data-related questions."}
    return csv_executor.invoke({"input": input_text})

router_tools = [
    Tool(
        name="Python Agent",
        func=python_agent_wrapper,
        description="""useful when you need to transform natural language to python and execute the python code,
                        returning the results of the code execution
                        DOES NOT ACCEPT CODE AS INPUT""",
    ),
    Tool(
        name="CSV Agent",
        func=csv_agent_wrapper,
        description="""useful when you need to answer question over episode_info.csv file,
                        takes an input the entire question and returns the answer after running pandas calculations""",
    ),
]

router_base_prompt = hub.pull("langchain-ai/react-agent-template")

router_prompt = router_base_prompt.partial(
    instructions="""You are a helpful router agent that directs requests to the appropriate specialized agent.
You have access to two agents:
1. Python Agent - Use this when you need to execute Python code or perform programming tasks
2. CSV Agent - Use this when you need to analyze or query the episode_info.csv file

For each request:
- Carefully analyze what type of task is being requested
- Choose the most appropriate agent based on the task requirements
- Direct the request to that agent using their specific tool
- Return the results to the user

Do not try to execute tasks directly - always route to the appropriate specialized agent."""
)
router_agent = create_react_agent(
    prompt=router_prompt,
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    tools=router_tools,
)
# Create memory for conversation history
router_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

router_agent_executor = AgentExecutor(
    agent=router_agent, 
    tools=router_tools, 
    memory=router_memory,
    verbose=True
)

