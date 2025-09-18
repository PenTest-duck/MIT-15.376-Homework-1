# MIT 15.376 HW #1: CrewAI Digital Twin Lite
[I like doing hackathons.](https://pentestduck.com/hackathons) The hardest thing about doing hackathons is coming up with an awesome idea. This CrewAI crew automates the process of researching ideas and planning it out.

## Run
1. Create a `.env` file and fill in the API keys (refer to `.env.example`).

2. Inside a virtual environment, install packages with `uv sync`.

3. To run, use `uv run main.py`.

A sample test run is provided in `REIMAGINE_DROPBOX.txt`, and the results are in `IDEAS.md`.

## Learnings / What Worked / What Broke

* Learnt how to use CrewAI agents in this "sprawled out" format of defining each task, then each agent, then the crew. I think the intended way nowadays is to create a `CrewBase` class and use markdown files for the agent and task descriptions.
* Making a multi-agent system is ridiculously easy nowadays
* Exa search was very simple to integrate and immediately useful (well done Exa!)
* Originally, I was going to build an email manager, and I tried to use Composio for Gmail integration but it didn't work for some strange reason. I learnt that Composio doesn't play well with CrewAI perhaps?
* CrewAI Enterprise integrations were still not ready for Google integrations as it was being blocked by Google

## Fun

Here is a selfie with me and Joao, co-founder of CrewAI, at the inaugural CrewAI hackathon in San Francisco:

![Joao and me](/joao.jpg)