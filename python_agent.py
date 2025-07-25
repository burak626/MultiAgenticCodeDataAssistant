from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool


load_dotenv()
 
# Python Agent Instructions
python_instructions = """You are an agent designed to write and execute python code to answer questions.
You have access to a python REPL, which you can use to execute python code.
If you get an error, debug your code and try again.
Only use the output of your code to answer the question.
You might know the answer without running any code, but you should still run the code to get the answer.

When generating files (like QR codes, plots, images), save them to the 'generated_files' directory.
For QR codes, use this pattern:
import qrcode
import os
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data('your_data_here')
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
os.makedirs('generated_files', exist_ok=True)
filename = 'qr_code_timestamp.png'
img.save(f'generated_files/{filename}')
print(f'QR code saved as {filename}. You can download it from the generated files section.')

If it does not seem like you can write code to answer the question, just return 
I don't know' as the answer."""

python_base_prompt = hub.pull("langchain-ai/react-agent-template")
python_prompt = python_base_prompt.partial(instructions=python_instructions)

python_tools = [PythonREPLTool()]

python_agent = create_react_agent(
    prompt=python_prompt,
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    tools=python_tools
)

# Python Agent Executor
python_executor = AgentExecutor(agent=python_agent, tools=python_tools, verbose=True)


