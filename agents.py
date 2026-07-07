from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

from tools import web_search,scrape_url

load_dotenv()

llm = init_chat_model(
    "gemini-1.5-flash",
    model_provider="google_genai",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 1st Agent
def built_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# 2nd Agent
def built_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# write chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clean, structured, and insightful reports."
    ),
    (
        "human",
        """
Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Requirements:
- Be detailed and factual
- Use professional tone
- Ensure clarity and structure
"""
    )
])

writer_chain=writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research critic and fact-checker. "
        "Your job is to carefully evaluate research reports for accuracy, clarity, structure, and completeness. "
        "Be strict but constructive."
    ),
    (
        "human",
        """
You are given a research report.

Your task is to critically review it and provide feedback.

Research Report:
{report}

Evaluate the report based on:

1. Accuracy (Are the claims factual and supported?)
2. Completeness (Is any important point missing?)
3. Structure (Is it well organized and readable?)
4. Clarity (Is it easy to understand?)
5. Sources (Are URLs properly included and relevant?)

Output format:

- Overall Score (0–10)
- Strengths (bullet points)
- Weaknesses (bullet points)
- Missing Information (if any)
- Fact-check Issues (if any)
- Final Suggestions for Improvement
"""
    )
])

critic_chain= critic_prompt | llm | StrOutputParser()