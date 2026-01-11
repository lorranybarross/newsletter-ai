from langchain.agents import create_agent
from src.agents.workflow import runWorkflow
from src.templates.prompts import full_prompt, createNewsletterPrompt
from src.tools.search import searchAndFilter
from src.core.llm import llm_model
from src.utils.exporter import exportToPDF

def main():
    topic = input('Qual tópico você gostaria de pesquisar hoje?\n')

    final_text = runWorkflow(topic)
    if final_text:
        exportToPDF(final_text)

if __name__ == '__main__':
    main()