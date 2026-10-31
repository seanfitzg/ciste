from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

small_model = init_chat_model(model="openai:gpt-5-nano")

big_model = init_chat_model(model="openai:gpt-6-luna")

response = small_model.invoke("What is the capital of France?")
print(response)

response = big_model.invoke("What is the capital of France?")
print(response)
