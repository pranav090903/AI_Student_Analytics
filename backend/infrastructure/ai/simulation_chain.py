from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from infrastructure.ai.llm import chat_model

simulation_prompt = ChatPromptTemplate.from_template("""
You are an academic performance advisor.

Original Prediction: {original_prediction}
New Prediction (after changes): {new_prediction}

Explain the impact of the changes in an encouraging way.
Provide actionable advice.
""")

simulation_chain = (
    simulation_prompt
    | chat_model
    | StrOutputParser()
)
