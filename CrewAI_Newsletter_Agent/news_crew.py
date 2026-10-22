
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Load API keys from .env
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from .env")

if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY is missing from .env")

model = os.getenv("MODEL", "openai/gpt-4o-mini")

# Tool available only to the Researcher
search_tool = SerperDevTool()

# 1. Researcher Agent
researcher = Agent(
    role="Technology News Researcher",
    goal="Find today's top 3 technology news stories using web search.",
    backstory=(
        "You are a careful technology journalist who finds current, "
        "reliable news and records the headline, source, date, and "
        "a short factual summary for each story."
    ),
    tools=[search_tool],
    llm=model,
    verbose=True
)

# 2. Writer Agent - no search tools
writer = Agent(
    role="Technology Newsletter Writer",
    goal="Write a concise newsletter based only on the research provided.",
    backstory=(
        "You are an experienced technology newsletter editor. "
        "You write clear, factual, engaging updates without adding "
        "unsupported information."
    ),
    tools=[],
    llm=model,
    verbose=True
)

# 3. Research Task
research_task = Task(
    description=(
        "Research today's top 3 technology news stories as of the "
        "current date. Use web search to find recent, credible reports. "
        "For each story, provide its headline, publication/source, "
        "publication date, and a concise factual summary. "
        "Do not invent stories or dates."
    ),
    expected_output=(
        "Exactly 3 numbered news stories. Each story must include "
        "a headline, source, publication date, and a 1-2 sentence "
        "summary. Include source URLs where available."
    ),
    agent=researcher
)

# 4. Writer Task - explicitly receives research_task output
newsletter_task = Task(
    description=(
        "Using ONLY the research output from the previous task, "
        "write a technology newsletter for today's readers. "
        "Select the three most important stories and summarize them "
        "clearly. Do not perform web searches or add unsupported facts."
    ),
    expected_output=(
        "Exactly 5 lines total: one headline followed by exactly "
        "4 bullet lines. The four bullets must summarize the news "
        "clearly. No blank lines, introduction, conclusion, or extra text."
    ),
    agent=writer,
    context=[research_task]
)

# 5. Run tasks sequentially
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, newsletter_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n===== FINAL 5-LINE NEWSLETTER =====\n")
    print(result.raw)
