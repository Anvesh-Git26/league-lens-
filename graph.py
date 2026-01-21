from typing import Dict, TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import END, StateGraph

# --- State Definition ---
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    web_search_needed: str # "Yes" or "No"

# --- Nodes ---

def retrieve(state):
    """
    Hybrid Retrieval: Fetches from Vector Store (Unstructured) and SQL (Structured).
    """
    print("---RETRIEVE---")
    question = state["question"]
    
    # Mock retrieval for the code skeleton
    documents = [f"Retrieved content for: {question}"] 
    return {"documents": documents, "question": question}

def grade_documents(state):
    """
    Determines if retrieved documents are relevant.
    """
    print("---CHECK RELEVANCE---")
    question = state["question"]
    documents = state["documents"]
    
    # Simple LLM grader logic would go here
    # For now, we assume documents are relevant
    return {"documents": documents, "question": question, "web_search_needed": "No"}

def generate(state):
    """
    Generates answer using LLM.
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "You are an expert Sports Analyst. Answer based on context: {context}. Question: {question}"
    )
    chain = prompt | llm
    response = chain.invoke({"context": documents, "question": question})
    return {"generation": response.content}

def transform_query(state):
    """
    Re-writes query if retrieval was bad.
    """
    print("---TRANSFORM QUERY---")
    question = state["question"]
    return {"question": f"Optimized {question}"}

def web_search(state):
    """
    Fallback to web search if local docs are insufficient.
    """
    print("---WEB SEARCH---")
    return {"documents": ["Web search results..."]}

# --- Conditional Edges ---

def decide_to_generate(state):
    """
    Decides whether to generate or use web search.
    """
    if state["web_search_needed"] == "Yes":
        return "web_search"
    return "generate"

# --- Graph Construction ---

workflow = StateGraph(GraphState)

# Add Nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)
workflow.add_node("web_search", web_search)

# Add Edges
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "web_search": "web_search",
        "generate": "generate",
    },
)
workflow.add_edge("web_search", "generate")
workflow.add_edge("transform_query", "retrieve")
workflow.add_edge("generate", END)

# Compile
app_graph = workflow.compile()