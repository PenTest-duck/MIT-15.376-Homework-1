"""
MIT AI Studio - CrewAI 
Author: Chris Yoo
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from exa_py import Exa
from dotenv import load_dotenv
from crewai_tools import FileWriterTool
load_dotenv()

# # Here is my failed attempt at using Composio
# from composio import Composio
# from composio_crewai import CrewAIProvider
# composio = Composio(provider=CrewAIProvider())
# email_tools = composio.tools.get(user_id="default", tools=[
#     "GMAIL_FETCH_EMAILS",
#     "GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID",
#     "GMAIL_FETCH_MESSAGE_BY_THREAD_ID",
# ])

# Exa search tool
@tool("Exa search and get contents")
def search_and_get_contents_tool(question: str) -> str:
    """Tool using Exa's Python SDK to run semantic search and return result highlights."""

    exa = Exa(os.getenv("EXA_API_KEY"))

    response = exa.search_and_contents(
        question,
        type="neural",
        num_results=3,
        highlights=True
    )

    parsedResult = ''.join([
      f'<Title id={idx}>{eachResult.title}</Title>'
      f'<URL id={idx}>{eachResult.url}</URL>'
      f'<Highlight id={idx}>{"".join(eachResult.highlights)}</Highlight>'
      for (idx, eachResult) in enumerate(response.results)
    ])

    return parsedResult


def create_research_agent():
    """Create a research agent that specializes in gathering information for potential hackathon ideas."""
    return Agent(
        role='Research Assistant',
        goal='To find and compile creative, unique, interesting, innovative, impactful hackathon ideas.',
        backstory="""You are a diligent research assistant with expertise in winning hackathons and performing idea research.
        You have a keen eye for creative, unique and interesting ideas on a given topic and can quickly identify the most promising ones.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_and_get_contents_tool]
    )

def create_plan_writer():
    """Create a plan writer agent that specializes in writing a detailed plan for a hackathon idea."""
    return Agent(
        role='Plan Writer',
        goal='To write a detailed plan for a hackathon idea in a file.',
        backstory="""You are a skilled plan writer with experience in writing detailed plans for hackathon ideas.
        You excel at taking a given hackathon idea and writing a detailed plan for it.""",
        verbose=True,
        allow_delegation=False,
        tools=[FileWriterTool()],
    )

def create_research_task(agent, topic):
    """Create a research task for the research agent."""
    return Task(
        description=f"""Research the topic: {topic}
        
        Your task is to:
        1. Research interesting parts or new trends about the topic
        2. Ideate on potential hackathon ideas based on the research
        3. Summarize your ideas in a list of 5 bullet points
        
        Focus on finding creative, unique, interesting, innovative, impactful hackathon ideas.""",
        expected_output="""A bullet point list of 10 hackathon ideas, each with 1-2 sentences describing the idea.""",
        agent=agent
    )

def create_plan_writer_task(agent):
    """Create a plan writer task for the plan writer agent."""
    return Task(
        description=f"""You are given a list of hackathon ideas.
        Choose a single idea, then create a well-structured plan and write it to a file `IDEAS.md`.""",
        expected_output="""A well-written plan inside `IDEAS.md` for the chosen hackathon idea containing:
        - Summary of the hackathon idea
        - A full evaluation (pros and cons) of the idea
        - A list of concrete steps to take to implement the idea
        - Any other relevant information
        - The idea must be chosen from the list of ideas provided in the research task""",
        agent=agent
    )

def main():
    """Main function to run the Crew AI example."""
    print("🚀 Starting CrewAI Hackathon Idea Generator")
    print("=" * 50)
    
    # Get topic from user input
    topic = input("Enter a topic for the hackathon: ")
    if not topic.strip():
        print("You must supply a topic")
        return
    
    print(f"\n📚 Topic: {topic}")
    print("=" * 50)
    
    # Create agents
    print("\n🤖 Creating AI agents...")
    researcher = create_research_agent()
    writer = create_plan_writer()
    
    # Create tasks
    print("📋 Setting up tasks...")
    research_task = create_research_task(researcher, topic)
    plan_writer_task = create_plan_writer_task(writer)
    
    # Create crew
    print("👥 Assembling the crew...")
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, plan_writer_task],
        process=Process.sequential,  # Tasks will be executed in sequence
        verbose=True
    )
    
    # Execute the crew
    print("\n🎯 Starting crew execution...")
    print("=" * 50)
    
    try:
        result = crew.kickoff()
        
        print("\n✅ Crew execution completed!")
        print("=" * 50)
        print("📄 Final Result:")
        print(result)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\n💡 Note: This example requires valid API keys to function properly.")
        print("Please set your OPENAI_API_KEY environment variable.")

if __name__ == "__main__":
    main()

