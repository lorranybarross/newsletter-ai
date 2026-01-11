from dotenv import load_dotenv
from datetime import datetime, timedelta
import chromadb
import json
import chromadb.utils.embedding_functions as embedding_functions
from langchain.tools import tool
from langchain_tavily import TavilySearch
from src.templates.prompts import createFilterAndParserChain
from src.core.llm import embeddings_model

N_OF_RESULTS = 10

load_dotenv()

embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction()
chroma_client = chromadb.PersistentClient('./data/')
collection = chroma_client.get_or_create_collection(name='newsletter_collection', embedding_function=embedding_function)

def searchAndFilter(topic: str):
    '''
    MANDATORY: Search and filter news about a specific topic.
    Every time the user asks to search, create or write about a topic,
    you MUST use this tool with 'topic' as argument.
    DO NOT call this tool more than once for the same topic.
    '''

    topic_vector = embeddings_model.embed_query(topic)
    collection_query = collection.query(query_embeddings=[topic_vector], n_results=1)

    if collection_query['ids'][0]:
        distance = collection_query['distances'][0][0]

        if distance < 0.1:
            metadata = collection_query['metadatas'][0][0]
            last_run = datetime.strptime(metadata['timestamp'], '%Y-%m-%d %H:%M:%S')

            if datetime.now() - last_run < timedelta(hours=24):
                print(f'--- Using embeddings for {topic} ---')
                return json.loads(collection_query['documents'][0][0])
    
    print(f'--- Using Tavily to search about {topic} ---')

    prompt = f'Busque pelos {N_OF_RESULTS} resultados mais recentes e revelantes sobre {topic} e retorne o título e um resumo do conteúdo de cada resultado.'

    search_tool = TavilySearch(max_result=N_OF_RESULTS, raw_content=True, search_depth='advanced')
    answer = search_tool.invoke({'query': prompt})

    chain = createFilterAndParserChain()
    filtered_results = chain.invoke({'search_results': answer})

    collection.add(
        embeddings=[topic_vector],
        documents=[json.dumps(filtered_results)],
        metadatas=[{'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}],
        ids=[topic],
    )

    return filtered_results