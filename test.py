from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM 

class_list = ["Math", "Science", "English", "History", "Art"]

# Create an Ollama LLM
llm = OllamaLLM(model="phi3")

# Define a prompt template
template = """
Generate a creative writing prompt based on the following class list:
{class_list}
"""

prompt = PromptTemplate(
    input_variables=["class_list"],
    template=template,
)

# Create an LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain
result = chain.run(class_list=class_list)

print(result)