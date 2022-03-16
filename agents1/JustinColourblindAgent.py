from typing import Dict
from agents1.BW4TBaselineAgent import BaseLineAgent

class JustinColourblindAgent(BaseLineAgent):
    def __init__(self, settings:Dict[str,object]):
        super().__init__(settings)

    def initialize(self):
        super().initialize()

    def filter_bw4t_observations(self, state):
        for objectDict in state.values():
            if 'visualization' in objectDict:
                objectDict['visualization']['colour'] = '#000000'
        return state

        
        print("This code in inside the filter_bw4t_observations method")