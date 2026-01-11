from datetime import datetime
from langsmith import Client
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.core.llm import llm_model
from src.models.schema import SearchResult

client = Client()

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Prompt for search on Tavily
hub_prompt = client.pull_prompt('hwchase17/react').template
system_instructions = '''
Você é um assistente que escreve newsletters. 
IMPORTANTÍSSIMO: Você NUNCA deve escrever sobre o tópico usando seu próprio conhecimento. 
Você DEVE sempre chamar a ferramenta 'searchAndFilter' primeiro para obter fatos reais. 
Somente após receber os dados da ferramenta, você escreverá a narrativa.

Hoje é dia {today}
'''
full_prompt = system_instructions + '\n\n' + hub_prompt

def createFilterAndParserChain():
    parser = JsonOutputParser(pydantic_object=SearchResult)

    prompt = PromptTemplate(
        template='''Você é um editor de notícias. Analise os resultados abaixo e selecione as 3 notícias mais relevantes.

        Resultados: {search_results}

        REGRAS:
        1. Ignore tutoriais e mercado financeiro.
        2. Retorne os resumos completos e detalhados.
        
        {format_instructions}''',
        input_variables=['search_results'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )

    chain = prompt | llm_model | parser
    return chain

def createNewsletterPrompt(topic: str, search_results: list):
    return f'''
    Você é um redator de newsletter versátil e curioso. Seu objetivo é escrever sobre "{topic}" de forma equilibrada e fluida.

    Use as informações retornadas pela sua ferramenta (RESULTADOS) para criar uma NARRATIVA ÚNICA.

    RESULTADOS: {search_results}
    
    ESTRUTURA EM MARKDOWN:
    1. # [Título chamativo e original]
    2. Introdução conectando o tema ao cotidiano.
    3. Desenvolvimento narrativo: integre as 3 notícias filtradas em um texto coeso. 
       - Use **negrito** para conceitos-chave.
       - Use *itálico* para analogias ou exemplos casuais.
    4. Conclusão com uma provocação final.
    5. ---
    6. ### Referências para se aprofundar:
       - Liste os títulos das notícias com seus respectivos links (URLs).
    '''