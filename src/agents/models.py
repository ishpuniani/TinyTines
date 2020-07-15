from abc import abstractmethod
from .helper import Helper


class AgentFactory:
    @classmethod
    def create_agent(cls, agent_dict):
        """
        This method returns an appropriate agent on the basis of the field "type" in the agent json
        :param agent_dict: The dictionary form of agent json element in the story
        :return: An agent of one of the types [HTTPRequestAgent, PrintAgent]
        :raises AttributeError: raises an exception if the type is something else.
        """
        agent_type = agent_dict['type']
        if agent_type == 'HTTPRequestAgent':
            return HTTPRequestAgent(agent_dict['name'], agent_dict['options'], agent_dict['options']['url'])
        elif agent_type == 'PrintAgent':
            return PrintAgent(agent_dict['name'], agent_dict['options'], agent_dict['options']['message'])
        else:
            raise AttributeError('Invalid agent type: ' + agent_type)


class Agent:
    """
    Base class for all agents.
    """

    def __init__(self, name, options):
        self.name = name
        self.options = options

    @abstractmethod
    def exec(self, op):
        """
        Abstract method that all subclasses need to define.
        :param op: the previous json output
        :return: The new json output on addition to or modification of the input json file.
        """
        raise NotImplementedError


class HTTPRequestAgent(Agent):
    def __init__(self, name, options, url):
        super().__init__(name, options)
        self.url = url

    def exec(self, op):
        """
        This method performs a get request and updates the input parameter with new key and response received.
        :param op: the previous json output
        :return: The new json output on addition to or modification of the input json file.
        """
        url = Helper.interpolate_values(self.url, op)
        output = Helper.get_request(url)
        op[self.name] = output
        return op


class PrintAgent(Agent):
    def __init__(self, name, options, message):
        super().__init__(name, options)
        self.message = message

    def exec(self, op):
        """
        This method prints the message mentioned in the story.
        :param op: the previous json output
        :return: Same as the input.
        """
        message = Helper.interpolate_values(self.message, op)
        print(message)
        return op
