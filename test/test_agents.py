import json
import unittest
from src.agents.models import AgentFactory


class TestAgents(unittest.TestCase):
    # Testing the create_agent method of AgentFactory
    def test_HTTPRequestAgent_creation(self):
        agent_dict = json.loads('{"type":"HTTPRequestAgent","name":"sunset","options":{'
                                '"url":"https:\/\/api.sunrise-sunset.org\/json?lat={{test_data.latitude}}&lng={{'
                                'test_data.longitude}}&date={{test_data.date}}"}}')
        agent = AgentFactory.create_agent(agent_dict)
        self.assertEqual(agent.__class__.__name__, "HTTPRequestAgent")

    def test_PrintAgent_creation(self):
        agent_dict = json.loads('{"type":"PrintAgent","name":"print","options":{"message":"Sunset in {{'
                                'location.city}}, {{location.country}} is at {{sunset.results.sunset}}."}}')
        agent = AgentFactory.create_agent(agent_dict)
        self.assertEqual(agent.__class__.__name__, "PrintAgent")

    def test_invalid_agent_creation(self):
        agent_dict = json.loads('{"type":"RandomAgent","name":"sunset","options":{'
                                '"url":"https:\/\/api.sunrise-sunset.org\/json?lat={{test_data.latitude}}&lng={{'
                                'test_data.longitude}}&date={{test_data.date}}"}}')
        self.assertRaises(AttributeError, AgentFactory.create_agent, agent_dict)
