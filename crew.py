from typing import List
from crewai import Agent,Crew,Task, LLM,Process
from crewai.project import CrewBase,agent,crew,task
from datetime import datetime
from crewai_tools import ScrapeWebsiteTool,DirectoryReadTool,FileWriterTool,FileReadTool
from pydantic import BaseModel,Field
from starlette.responses import Content

# yahan custom scrapingdog tool import karo
from scrapingdog_tool import scrapingdog_search

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
import nest_asyncio

# Apply nest_asyncio to fix event loop issues
nest_asyncio.apply()

# os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm=LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    #provider="google",
    temperature=0.7,
    timeout=120 # api call kr k 120 sec wait kro (good for long responses and slow internet connections)
)
# content class is a pydantic model
class Content(BaseModel):
    content_type: str = Field(
        ..., description="The type of content to be created (e.g., blog post, social media post, video)")
    topic: str = Field(..., description="The topic of the content")
    target_audience: str = Field(..., description="The target audience for the content")
    tags: List[str] = Field(..., description="Tags to be used for the content")
    content: str = Field(..., description="The content itself")


@CrewBase
class TheMarketingCrew():
    agents_config="config/agents.yaml"
    tasks_config="config/tasks.yaml"

    #agent 1 of marketing:
    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config=self.agents_config['head_of_marketing'],
            tools=[scrapingdog_search ,ScrapeWebsiteTool(),DirectoryReadTool('resources/drafts'),FileWriterTool(),FileReadTool()],
            # resources folder h aur drafts b usky andr ek folder h
            reasoning=True,  #
            inject_date=True,  # Current date: {current_date} yeh yaml ma h yeh inject hogi lastest date
            llm=llm,
            allow_delegation=True,
            max_rpm=3
        )
    @agent
    def content_creator_social_media(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator_social_media'],
            tools=[scrapingdog_search ,ScrapeWebsiteTool(),DirectoryReadTool('resources/drafts'),FileWriterTool(),FileReadTool()],
            inject_date=True, llm=llm,
            allow_delegation=True,
            max_rpm=3,
            max_iter=30
        )

    @agent
    def content_writer_blogs(self)-> Agent:
        return Agent(
            config=self.agents_config['content_writer_blogs'],
            tools=[scrapingdog_search,ScrapeWebsiteTool(),DirectoryReadTool('resources/drafts/blogs'),FileWriterTool(),FileReadTool()],
            inject_date=True, llm=llm,
            allow_delegation=True,
            max_rpm=3,
            max_iter=5
        )
    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            tools=[scrapingdog_search,ScrapeWebsiteTool(),DirectoryReadTool('resources/drafts'),FileWriterTool(),FileReadTool()],
            reasoning=True, inject_date=True, llm=llm,
            allow_delegation=True,
            max_rpm=3,
            max_iter=3
        )
    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config['market_research'],
            agent=self.head_of_marketing()
        )
    @task
    def  prep_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_marketing_strategy'],
            agent=self.head_of_marketing()
        )
    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config['create_content_calendar'],
            agent=self.content_creator_social_media()
        )
    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_post_drafts'],
            agent=self.content_creator_social_media(),
            output_json=Content
        )
    @task
    def prep_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_scripts_for_reels'],
            agent=self.content_creator_social_media(),
            output_json=Content
        )
    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config=self.tasks_config['content_research_for_blogs'],
            agent=self.content_writer_blogs(),
            output_json=Content
        )
    @task
    def draft_blogs(self) -> Task:
        return Task(
            config=self.tasks_config['draft_blogs'],
            agent=self.content_writer_blogs(),
            output_json=Content
        )
    @task
    def seo_optimization(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization'],
            agent=self.seo_specialist(),
            output_json=Content
        )
    @crew

    def marketingcrew(self) -> Crew:
        return Crew(
            # it takes all the agents from the yaml file
            agents=self.agents,
            # it takes all the tasks from the yaml file
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,
            max_rpm=3
        )
