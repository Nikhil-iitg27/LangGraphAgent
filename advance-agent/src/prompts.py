class ResearchDiscoveryPrompts:
    """
    Prompts for extracting and summarizing the latest technological advancements for a given academic field and subtopic.
    Designed for use with the ResearchDiscoveryState and ResearchAdvancement models.
    """

    # STEP 1: SYSTEM prompt for extracting a list of advancement titles (free-form LLM)
    ADVANCEMENT_TITLES_SYSTEM = """
You are an expert academic research assistant. Given recent articles, blogs, and research paper abstracts, extract a list of the most significant advancements, discoveries, or breakthroughs in the specified field and subtopic. Focus on content from 2024 and later.
Return only the titles (and, if available, a main link) for each advancement, one per line.
"""

    @staticmethod
    def advancement_titles_user(field: str, subtopic: str, content: str) -> str:
        return f"""
Field: {field}
Subtopic: {subtopic}
Content:
{content}

Instructions:
- Extract 5-10 of the most recent and significant advancements, discoveries, or breakthroughs in this subtopic.
- For each, return:
    * title: Concise title of the advancement or paper
    * main_link: (optional) Main link to the paper, blog, or resource
- Return as a plain list, one advancement per line, in the format: "Title [main_link]"
"""

    # STEP 2: SYSTEM prompt for extracting full details for a single advancement (structured LLM)
    ADVANCEMENT_DETAIL_SYSTEM = """
You are an expert academic research assistant. Given the title and content of a recent advancement, extract all relevant details as defined in the ResearchAdvancement Pydantic model. Focus on accuracy and completeness.
"""

    @staticmethod
    def advancement_detail_user(title: str, content: str) -> str:
        return f"""
Advancement Title: {title}
Content:
{content}

Instructions:
- Extract all fields required by the ResearchAdvancement model for this advancement:
    * title: The full, official title of the advancement or research paper.
    * summary: A clear, detailed summary of the advancement (2-4 sentences) describing the main contribution, findings, or result.
    * authors: List of all author names (first and last names, separated; include all if possible).
    * keywords: List of key topics, methods, or technologies relevant to the advancement (e.g., “transformers”, “Genetic Engineering”, “Hydrogen Bonding”, “Graph Theory”).
    * impact_statement: 1-2 sentences on the significance, novelty, or potential impact of this work for the field or community.
    * language: The primary language of the paper or resource (e.g., English, Chinese, Spanish).
    * paper_links: List of URLs to official research papers (arXiv, IEEE, Nature, etc.).
    * blog_links: List of URLs to relevant blogs, technical articles, or news coverage.
    * pdf_links: List of direct URLs to downloadable PDFs (main paper, supplementary, etc.).
    * code_links: List of URLs to open-source code or implementations (GitHub, GitLab, etc.).
    * date: Year or full date of publication (YYYY or YYYY-MM-DD).
- If a field is not available, use null or an empty list as appropriate.
- Return the result as object matching the ResearchAdvancement model.
"""

    # SYSTEM prompt for synthesizing trends and future directions
    SYNTHESIS_SYSTEM = """
You are an academic research analyst. Synthesize the extracted advancements to identify overall trends, emerging themes, and possible future directions in the subtopic. Your synthesis should be actionable and reference the provided advancements.
"""

    @staticmethod
    def synthesis_user(field: str, subtopic: str, advancements: str) -> str:
        return f"""
Field: {field}
Subtopic: {subtopic}
Advancements (Python object or list):
{advancements}

Instructions:
- Write a synthesis paragraph (5-7 sentences) summarizing:
    * Key trends and themes in recent advancements
    * Notable breakthroughs or shifts in research focus
    * Gaps, challenges, or open problems
    * Possible future research directions
- Reference specific advancements, authors, or keywords where relevant.
- Focus on insights relevant to researchers and practitioners in this subtopic.
"""