from typing import Dict, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .firecrawl import FirecrawlService
from .prompts import ResearchDiscoveryPrompts
from .models import ResearchDiscoveryState, ResearchAdvancement, ResearchDiscoveryOutput
import logging

class Workflow:
    def __init__(self):
        self.logger = logging.getLogger("ResearchWorkflow")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s in %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        self.logger.propagate = False

        self.firecrawl = FirecrawlService()
        self.logger.info("FirecrawlService initialized.")

        model = "gpt-4o"
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.1
        )
        self.logger.info(f"OpenAI {model} initialized.")

        self.prompts = ResearchDiscoveryPrompts()
        self.state_cls = ResearchDiscoveryState
        self.workflow = self._build_workflow()
        self.logger.info("Workflow Build Complete.")
    
    def _build_workflow(self):
        graph = StateGraph(self.state_cls)
        graph.add_node("search_sources", self._search_sources_step)
        graph.add_node("extract_titles", self._extract_titles_step)
        graph.add_node("extract_details", self._extract_details_step)
        graph.add_node("synthesize", self._synthesize_step)

        graph.add_edge(START, "search_sources")
        graph.add_edge("search_sources", "extract_titles")
        graph.add_edge("extract_titles", "extract_details")
        graph.add_edge("extract_details", "synthesize")
        graph.add_edge("synthesize", END)

        return graph.compile()
    
    def _search_sources_step(self, state:ResearchDiscoveryState) -> Dict[str, List[Dict]]:
        self.logger.info(f"Searching sources for: {state.query}")
        try:
            search_results = self.firecrawl.search_research_content(state.query, num_results=10)
            self.logger.info(f"Found {len(search_results)} sources.")
            return {"search_results": search_results}
        except Exception as e:
            self.logger.error(f"Error in _search_sources_step: {e}", exc_info=True)
            return {"error_logs": [str(e)]}

    def _extract_titles_step(self, state:ResearchDiscoveryState) -> Dict[str, List[Dict]]:
        self.logger.info("Extracting advancement titles from sources.")
        try:
            all_content = "\n\n".join([src.get('snippet', '') for src in state.search_results])
            field, subtopic = (state.query.split('->') + [None, None])[:2]
            messages = [
                SystemMessage(content=self.prompts.ADVANCEMENT_TITLES_SYSTEM),
                HumanMessage(content=self.prompts.advancement_titles_user(field.strip() if field else '', subtopic.strip() if subtopic else '', all_content))
            ]
            response = self.llm.invoke(messages)
            titles = []
            for line in response.content.strip().split("\n"):
                if line.strip():
                    if '[' in line and ']' in line:
                        title, link = line.rsplit('[', 1)
                        main_link = link.strip(' ]') or ""
                        titles.append({'title': title.strip(), 'main_link': main_link})
                    else:
                        titles.append({'title': line.strip(), 'main_link': ""})
            self.logger.info(f"Extracted {len(titles)} advancement titles.")
            return {"advancement_titles": titles}
        except Exception as e:
            self.logger.error(f"Error in _extract_titles_step: {e}", exc_info=True)
            return {"error_logs": [str(e)]}

    def _extract_details_step(self, state:ResearchDiscoveryState) -> Dict[str, List[ResearchAdvancement]]:
        self.logger.info("Extracting detailed advancement information.")
        advancements = []
        errors = []
        try:
            for adv in state.advancement_titles:
                related_contents = []
                for src in state.search_results:
                    if adv['main_link'] and adv['main_link'] in src.get('url', ''):
                        related_contents.append(src.get('snippet', ''))
                    elif adv['title'].lower() in src.get('title', '').lower():
                        related_contents.append(src.get('snippet', ''))
                combined_content = "\n\n".join(related_contents)
                if not combined_content:
                    self.logger.warning(f"No content found for advancement: {adv['title']}")
                try:
                    messages = [
                        SystemMessage(content=self.prompts.ADVANCEMENT_DETAIL_SYSTEM),
                        HumanMessage(content=self.prompts.advancement_detail_user(adv['title'], combined_content))
                    ]
                    # Use function_calling method to avoid OpenAI schema issues
                    structured_llm = self.llm.with_structured_output(ResearchAdvancement, method="function_calling")
                    advancement = structured_llm.invoke(messages)
                    advancements.append(advancement)
                except Exception as e:
                    self.logger.error(f"Error extracting details for {adv['title']}: {e}", exc_info=True)
                    errors.append(f"{adv['title']}: {e}")
            self.logger.info(f"Extracted details for {len(advancements)} advancements.")
            return {"advancements": advancements, "error_logs": errors}
        except Exception as e:
            self.logger.error(f"Error in _extract_details_step: {e}", exc_info=True)
            return {"error_logs": [str(e)]}

    def _synthesize_step(self, state:ResearchDiscoveryState) -> Dict[str, str]:
        self.logger.info("Synthesizing overall trends and future directions.")
        try:
            field, subtopic = (state.query.split('->') + [None, None])[:2]
            messages = [
                SystemMessage(content=self.prompts.SYNTHESIS_SYSTEM),
                HumanMessage(content=self.prompts.synthesis_user(
                    field.strip() if field else '',
                    subtopic.strip() if subtopic else '',
                    state.advancements
                ))
            ]
            response = self.llm.invoke(messages)
            self.logger.info("Synthesis complete.")
            return {"synthesis": response.content}
        except Exception as e:
            self.logger.error(f"Error in _synthesize_step: {e}", exc_info=True)
            return {"error_logs": [str(e)]}
            
    
    
    def run(self, query: str) -> ResearchDiscoveryState:
        self.logger.info(f"Starting research workflow for query: {query}")
        initial_state = self.state_cls(query=query)
        try:
            final_state = self.workflow.invoke(initial_state)
            self.logger.info("Workflow completed successfully.")
            return self.state_cls(**final_state)
        except Exception as e:
            self.logger.critical(f"Workflow failed: {e}", exc_info=True)
            return self.state_cls(query=query, error_logs=[str(e)])