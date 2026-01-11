from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import src.tools.search as tools
import src.templates.prompts as prompts
from src.core.llm import llm_model

class State(TypedDict):
    topic: str
    prompt: str
    final_text: str
    search_results: list 

def checkResults(state: State):
    '''Check if returned results.'''
    if not state['search_results'] or len(state['search_results']) == 0:
        return 'Failed'
    return 'Successful'

def useSearchAndFilterTool(state: State):
    '''Uses search and filter tool about a specific topic.'''
    search_results = tools.searchAndFilter(state['topic'])
    return {'search_results': search_results}

def getPrompt(state: State):
    '''Get prompt to use on agent.'''
    prompt = prompts.createNewsletterPrompt(state['topic'], state['search_results'])
    return {'prompt': prompt}

def getFinalText(state: State):
    '''Invoke agent and convert answer to markdown.'''
    response = llm_model.invoke(state['prompt'])
    final_text = response.content
    return {'final_text': final_text}

def runWorkflow(topic: str):
    workflow = StateGraph(State)

    workflow.add_node('search_and_filter', useSearchAndFilterTool)
    workflow.add_node('get_prompt', getPrompt)
    workflow.add_node('get_final_text', getFinalText)

    workflow.add_edge(START, 'search_and_filter')
    workflow.add_conditional_edges(
        'search_and_filter', checkResults, {'Failed': END, 'Successful': 'get_prompt'}
    )
    workflow.add_edge('get_prompt', 'get_final_text')
    workflow.add_edge('get_final_text', END)

    chain = workflow.compile()
    state = chain.invoke({'topic': topic})

    return state.get('final_text')    