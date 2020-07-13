import json

from agents.models import AgentFactory


class Story:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path) as f:
            story = json.load(f)

        self.agents = story['agents']

    def run(self):
        op = ''
        for agent_dict in self.agents:
            agent = AgentFactory.create_agent(agent_dict)
            op = agent.exec(op)
