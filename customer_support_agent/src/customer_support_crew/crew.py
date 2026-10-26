from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from .tools.google_sheet_tool import log_to_google_sheet
from .tools.rag_tool import rag_tool

@CrewBase
class CustomerSupportCrew():
    """CustomerSupportCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def rag_support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['rag_support_agent'],
            tools=[rag_tool],
            verbose=True
        )

    @agent
    def web_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_search_agent'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def google_sheet_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['google_sheet_agent'],
            tools=[log_to_google_sheet],
            verbose=True
        )

    @task
    def rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['rag_task'],
        )

    @task
    def web_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_search_task'],
        )

    @task
    def sheet_logging_task(self) -> Task:
        return Task(
            config=self.tasks_config['sheet_logging_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
