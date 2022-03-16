from typing import final, List, Dict, Final
import enum, random
import bisect

from agents1.BW4TBaselineAgent import BaseLineAgent
from bw4t.BW4TBrain import BW4TBrain
from matrx.agents.agent_utils.state import State
from matrx.agents.agent_utils.navigator import Navigator
from matrx.agents.agent_utils.state_tracker import StateTracker
from matrx.actions.door_actions import OpenDoorAction
from matrx.actions.object_actions import GrabObject, DropObject
from matrx.messages.message import Message

# Actions
from matrx.actions.action import Action, ActionResult
from matrx.actions.door_actions import OpenDoorAction, OpenDoorActionResult, CloseDoorAction, CloseDoorActionResult
from matrx.actions.move_actions import MoveActionResult, MoveNorth, MoveNorthEast, MoveSouthEast, MoveSouth, \
    MoveSouthWest, MoveWest, MoveNorthWest, MoveEast
from matrx.actions.object_actions import RemoveObject, RemoveObjectResult, GrabObject, GrabObjectResult, \
    DropObject, DropObjectResult

# open doors (if needed) -> get proper block -> bring it to drop off location -> check if indeed this block is now needed -> drop it off.

class JustinStrongAgent(BaseLineAgent):
    PLAN_PATH_TO_CLOSED_DOOR=1,
    FOLLOW_PATH_TO_CLOSED_DOOR=2,
    OPEN_DOOR=3


    def __init__(self, settings:Dict[str,object]):
        super().__init__(settings)

        # An ordered list of target blocks we need to provide in that order.
        self.targetBlocks = []
        self.amountOfTargetBlocks = 0

    def initialize(self):
        super().initialize()

    def filter_bw4t_observations(self, state):
        self._processMessages(self, teamMembers)
        print("This code in inside the filter_bw4t_observations method")
        return state

    def decide_on_bw4t_action(self, state:State):
        self._storeTargetBlocks(state)

        agent_name = state[self.agent_id]['obj_id']
        # Add team members
        for member in state['World']['team_members']:
            if member!=agent_name and member not in self._teamMembers:
                self._teamMembers.append(member)
                # Process messages from team members
        receivedMessages = self._processMessages(self._teamMembers)
        # Update trust beliefs for team members
        self._trustBlief(self._teamMembers, receivedMessages)

        return (MoveSouth.__name__, {})

    """
    This method takes the target blocks from the state and stores them in the variable self.targetBlocks. It also stores the
    amount of target blocks we have to get in self.amountOfTargetBlocks 
    """
    def _storeTargetBlocks(self, state:State):
        self.targetBlocks = [object for object in state.values() if 'is_goal_block' in object and object['is_goal_block']]
        self.targetBlocks = sorted(self.targetBlocks, key=lambda x: x['location'][1], reverse=True)
        self.amountOfTargetBlocks = len(self.targetBlocks)

    """
    Together, these sendMessage methods contain a method for any action that the agent can do. The adhere to the format
    as stated in the assignment. They contain at least the messages that are required by the assignment.
    """
    def _sendMessageMovingToRoom(self, room_name, to_id=None):
        message = "Moving to " + room_name
        self._sendMessage(message, self.agent_id, to_id)

    def _sendMessageOpeningDoorOfRoom(self, room_name, to_id=None):
        message = "Opening door of " + room_name
        self._sendMessage(message, self.agent_id, to_id)

    def _sendMessageSearchingThroughRoom(self, room_name, to_id=None):
        message = "Searching through " + room_name
        self._sendMessage(message, self.agent_id, to_id)

    def _sendMessageFoundGoalBlockAtLocation(self, visualization, location, to_id=None):
        message = "Found goal block " + visualization + " at location " + location
        self._sendMessage(message, self.agent_id, to_id)

    def _sendMessagePickingUpGoalBlockAtLocation(self, visualization, location, to_id=None):
        message = "Picking up goal block " + visualization + " at location " + location
        self._sendMessage(message, self.agent_id, to_id)

    def _sendMessageDroppedGoalBlockAtLocation(self, visualization, location, to_id=None):
        message = "Dropped goal block " + visualization + " at drop location " + location
        self._sendMessage(message, self.agent_id, to_id)





# def _sendMessage(self, mssg, sender):
#     '''
#     Enable sending messages in one line of code
#     '''
#     msg = Message(content=mssg, from_id=sender)
#     if msg.content not in self.received_messages:
#         self.send_message(msg)

    # def _sendMessage(self, mssg, sender):
    # def _processMessages(self, teamMembers):
    # def _trustBlief(self, member, received):

