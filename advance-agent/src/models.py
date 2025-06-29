from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl

# Represents a single research advancement in the subtopic
class ResearchAdvancement(BaseModel):
    title: str  # Title of the advancement or paper
    summary: str  # Detailed summary of the advancement
    authors: List[str] = []  # List of author names
    keywords: List[str] = []  # List of keywords or topics
    impact_statement: Optional[str] = None  # Short statement on significance/impact
    language: Optional[str] = None  # Language of the paper or resource
    paper_links: List[str] = []  # Links to research papers (arXiv, IEEE, etc.)
    blog_links: List[str] = []  # Links to blogs or technical articles
    pdf_links: List[str] = []  # Direct links to PDFs if available
    code_links: List[str] = []  # Open-source implementation links (GitHub, etc.)
    date: Optional[str] = None  # Publication date or year


# Represents the overall output for a query
class ResearchDiscoveryOutput(BaseModel):
    field: str  # e.g., "Computer Science"
    subtopic: str  # e.g., "Distributed Systems"
    advancements: List[ResearchAdvancement]  # List of recent advancements
    synthesis: str  # Synthesis paragraph summarizing trends and future directions
    search_time: Optional[str] = None  # Timestamp or duration of the search


# State object for LangGraph workflow
class ResearchDiscoveryState(BaseModel):
    query: str  # "Field -> Subtopic"
    search_results: List[Dict[str, Any]] = []  # Raw search results from Firecrawl
    advancement_titles: List[Dict[str, str]] = []  # List of titles and main links for advancements.
    advancements: List[ResearchAdvancement] = []  # Structured advancements
    synthesis: Optional[str] = None  # Synthesis paragraph
    output: Optional[ResearchDiscoveryOutput] = None  # Final structured output
    error_logs: List[str] = []  # Errors or warnings encountered during workflow
    progress: Optional[str] = None  # Status or progress indicator