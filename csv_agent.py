from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain_experimental.agents.agent_toolkits import create_csv_agent


load_dotenv()

# CSV Agent Instructions
csv_instructions = """You are an agent designed to analyze and work with CSV data files.
You have access to tools that can read, analyze, and manipulate CSV files.
When working with CSV data, always provide clear and accurate information about the data structure.
If you encounter any errors while processing the CSV file, debug and try alternative approaches.
Always base your answers on the actual data in the CSV file.
If you cannot find the requested information in the CSV file, clearly state what data is available."""

csv_base_prompt = hub.pull("langchain-ai/react-agent-template")
csv_prompt = csv_base_prompt.partial(instructions=csv_instructions)

# CSV Agent Executor - Initially None, will be created when CSV is uploaded
csv_executor = None