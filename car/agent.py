import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q = {}
        self.random_action_value = 100.0
        self.actions = [None, 'right', 'forward', 'left']
        self.alpha = 0.5
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        if self.random_action_value < 1.0:
            self.random_action_value = 0.0 #Avoid random actions after a certain threshold
        else:
            self.random_action_value = self.random_action_value - 1.0 #Reduce the frequency of random actions

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        # TODO: Update state
        self.state = (self.next_waypoint,inputs['light'],inputs['oncoming'],inputs['left'])#,inputs['right'],deadline)
        
        # TODO: Select action according to your policy
        #action = None
        #action = self.next_waypoint
        #action = [None, 'forward', 'left', 'right'][random.randint(0,3)]
        Q = [self.q.get((self.state, a), self.random_action_value) for a in self.actions] #Find Q values based on possible actions, defaults to self.random_action_value
        maxQ = max(Q) #Find the max Q value
        i = Q.index(maxQ) #Find the index of the Q value
        action = self.actions[i]        
        
        # Execute action and get reward
        reward = self.env.act(self, action)
        
        # TODO: Learn policy based on state, action, reward
        old_value = self.q.get((self.state, action), None)
        if old_value == None:
            self.q[(self.state, action)] = reward
        else:
            self.q[(self.state, action)] = (1 - self.alpha) * old_value + self.alpha * reward
        
        #print self.q
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
