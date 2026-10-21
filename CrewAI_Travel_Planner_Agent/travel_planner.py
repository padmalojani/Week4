import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables from .env
load_dotenv()

# Validate configuration
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from .env")

model = os.getenv("MODEL", "openai/gpt-4o-mini")


# 1. Create the Travel Planner Agent
travel_planner = Agent(
    role="Travel Planner",
    goal="Recommend exactly three worthwhile places to visit in the city provided by the user.",
    backstory=(
        "You are an experienced travel planner who helps first-time visitors "
        "discover a city's most interesting attractions. You write for travelers "
        "who want practical, concise recommendations rather than lengthy essays. "
        "You explain why each place is worth visiting and avoid inventing facts."
    ),
    llm=model,
    verbose=True
)


# 2. Ask the user for a city
city = input("Enter the city you want to explore: ").strip()

if not city:
    raise ValueError("City name cannot be empty.")


# 3. Create the Task
travel_task = Task(
    description=(
        f"Recommend exactly three places to visit in {city}. "
        "Choose places that are relevant to visitors and provide useful variety. "
        "Do not recommend places outside the requested city. "
        "If you are uncertain about a fact, do not invent it."
    ),
    expected_output=(
        "Return exactly three numbered recommendations, numbered 1 to 3. "
        "For each recommendation, include the place name, its location or area "
        "if known, and one or two sentences explaining why a visitor should go. "
        "Use clear, concise language. Do not include an introduction, a conclusion, "
        "or any additional recommendations."
    ),
    agent=travel_planner
)


# 4. Assemble the Crew
travel_crew = Crew(
    agents=[travel_planner],
    tasks=[travel_task],
    process=Process.sequential,
    verbose=True
)


# 5. Run the Crew and print the result
result = travel_crew.kickoff()

print("\n===== YOUR TRAVEL PLAN =====\n")
print(result)