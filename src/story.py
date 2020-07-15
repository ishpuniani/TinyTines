import json

from agents.models import AgentFactory


class Story:
    """
    Class to load the story file and import all the relevant properties, in this case the agents
    """
    def __init__(self, file_path):
        self.file_path = file_path
        with open(self.file_path) as f:
            story = json.load(f)

        self.agents = story['agents']

    def run(self):
        """
        This method runs the story serially.
        Different agents are executed one-by-one.
        The story stops executing if one of the agents raises an exception.
        """
        op = {}
        for agent_dict in self.agents:
            try:
                agent = AgentFactory.create_agent(agent_dict)
                op = agent.exec(op)
            except AttributeError as ae:
                print("Invalid agent syntax! Please check: " + agent_dict["name"])
                print(ae)
                break
            except Exception as e:
                print("Unable to process agent: " + agent_dict["name"])
                # raise e
                print(e)
                break
