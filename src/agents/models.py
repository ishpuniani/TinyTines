from abc import abstractmethod


class AgentFactory:
    @classmethod
    def create_agent(cls, agent_dict):
        agent_type = agent_dict['type']
        if agent_type == 'HTTPRequestAgent':
            print("Creating HTTPRequestAgent")
            return HTTPRequestAgent(agent_dict['name'], agent_dict['options'], agent_dict['options']['url'])
        elif agent_type == 'PrintAgent':
            print("Creating PrintAgent")
            return PrintAgent(agent_dict['name'], agent_dict['options'], agent_dict['options']['message'])
        else:
            raise AttributeError('Invalid agent type: ' + agent_type)


class Agent:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    @abstractmethod
    def exec(self, op): raise NotImplementedError


class HTTPRequestAgent(Agent):
    def __init__(self, name, options, url):
        super().__init__(name, options)
        self.url = url

    def exec(self, op):
        print("HTTPRequestAgent::Exec")


class PrintAgent(Agent):
    def __init__(self, name, options, message):
        super().__init__(name, options)
        self.message = message

    def exec(self, op):
        print("PrintAgent::Exec")
