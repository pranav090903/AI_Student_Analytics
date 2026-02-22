from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task='text generation',
    max_new_tokens=400,
    temperature=0.4
)
chat_model=ChatHuggingFace(llm=llm)
