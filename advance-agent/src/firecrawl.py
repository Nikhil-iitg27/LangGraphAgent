import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
import logging

load_dotenv()

class FirecrawlService:
    """
    Service for searching and scraping web content using Firecrawl, adapted for academic research and advancements analysis.
    """

    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")

        self.logger = logging.getLogger("Firecrawl")
        self.logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers if re-imported in notebooks or scripts
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

        if not api_key:
            self.logger.critical("Missing FIRECRAWL_API_KEY environment variable. FirecrawlService will not function.")
            raise ValueError("FIRECRAWL_API_KEY environment variable is required.")

        try:
            self.app = FirecrawlApp(api_key=api_key)
            self.logger.info("FirecrawlApp initialized successfully.")
        except Exception as e:
            self.logger.critical(f"Failed to initialize FirecrawlApp: {e}")
            raise

    def search_research_content(self, query: str, num_results: int = 10):
        """
        Search for recent research papers, blogs, and technical content related to the query.
        Returns a list of dicts with at least 'title', 'url', and 'snippet' for each result.
        """
        try:
            self.logger.info(f"Searching for research content: query='{query}', num_results={num_results}")
            result = self.app.search(
                query=f"{query} research advancements 2024 2025 arXiv IEEE Nature blog github",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            if hasattr(result, 'data'):
                self.logger.info(f"Search completed. {len(result.data)} results found.")
                # Normalize results for downstream use
                normalized = []
                for entry in result.data:
                    normalized.append({
                        'title': entry.get('metadata', {}).get('title', ''),
                        'url': entry.get('url', ''),
                        'snippet': entry.get('markdown', '')[:1000],
                        'raw': entry
                    })
                return normalized
            else:
                self.logger.warning("No data attribute in Firecrawl search result.")
                return []
        except Exception as e:
            self.logger.error(f"Error during search_research_content: {e}", exc_info=True)
            return []

    def scrape_research_page(self, url: str) -> dict:
        """
        Scrape the content of a research paper, blog, or technical page by URL.
        Returns a dict with at least 'markdown', 'url', and 'status'.
        """
        try:
            self.logger.info(f"Scraping URL: {url}")
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            if result and hasattr(result, 'markdown') and result.markdown:
                self.logger.info(f"Scraping successful for URL: {url} (content length: {len(result.markdown)})")
                return {
                    'url': url,
                    'markdown': result.markdown,
                    'status': 'success',
                    'raw': result
                }
            else:
                self.logger.warning(f"Scraping returned no markdown content for URL: {url}")
                return {
                    'url': url,
                    'markdown': '',
                    'status': 'no_content',
                    'raw': result
                }
        except Exception as e:
            self.logger.error(f"Error during scrape_research_page for URL {url}: {e}", exc_info=True)
            return {
                'url': url,
                'markdown': '',
                'status': 'error',
                'error': str(e)
            }