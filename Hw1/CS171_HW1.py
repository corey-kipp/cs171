import random
import collections

class Thing(object):

    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want.  Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        "Things that are 'alive' should return true."
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        "Display the agent's internal state.  Subclasses should override."
        print("I don't know how to show_state.")

    def display(self, canvas, x, y, width, height):
        # Do we need this?
        "Display an image of this Thing on the canvas."
        pass


class Agent(Thing):

    """An Agent is a subclass of Thing with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method.  If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts.  An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None:
            def program(percept):
                return eval(input('Percept={}; action? ' .format(percept)))
        assert isinstance(program, collections.Callable)
        self.program = program

    def can_grab(self, thing):
        """Returns True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


def TraceAgent(agent):
    """Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment."""
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print('{} perceives {} and does {}'.format(agent, percept, action))
        return action
    agent.program = new_program
    return agent
class Environment(object):

    """Abstract class representing an Environment.  'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        '''
            Return the percept that the agent sees at this point.
            (Implement this.)
        '''
        raise NotImplementedError

    def execute_action(self, agent, action):
        "Change the world to reflect this action. (Implement this.)"
        raise NotImplementedError

    def default_location(self, thing):
        "Default location to place a new thing with unspecified location."
        return None

    def exogenous_change(self):
        "If there is spontaneous change in the world, override this."
        pass

    def is_done(self):
        "By default, we're done when we can't find a live agent."
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        "Run the Environment for given number of time steps."
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}" .format(thing, thing.location))
            print("  from list: {}" .format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)
class Dirt(Thing):
    pass

class TrivialVacuumEnvironment(Environment):

    """This environment has two locations, A and B. Each can be Dirty
    or Clean.  The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self, performance_measure_type = 'default'):
        super(TrivialVacuumEnvironment, self).__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty']),
                       loc_C: random.choice(['Clean', 'Dirty'])
                      }
        self.performance_measure_type = performance_measure_type
        
    def thing_classes(self):
        return [Dirt, ReflexVacuumAgent, RandomVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action):
        "Change the world to reflect this action. (Implement this.)"
        if action == 'Right':
          if self.performance_measure_type != 'default':
            agent.performance -= 1
          if agent.location == loc_A:
            agent.location = loc_B
          elif agent.location == loc_B:
            agent.location = loc_C
          else:
            agent.location = loc_C
            
        elif action == 'Left':
          if self.performance_measure_type != 'default':
            agent.performance -= 1
          if agent.location == loc_A:
            agent.location = loc_A
          elif agent.location == loc_B:
            agent.location = loc_A
          elif agent.location == loc_C:
            agent.location = loc_B
        
        elif action == 'Suck':
          if self.performance_measure_type != 'default':
            if self.status[agent.location] == 'Dirty':
              agent.performance += 10
          self.status[agent.location] = 'Clean'
        
        
        if self.performance_measure_type == 'default':
          if self.status[loc_A] == 'Clean':
            agent.performance += 1
          if self.status[loc_B] == 'Clean':
            agent.performance += 1
          if self.status[loc_C] == 'Clean':
            agent.performance += 1

    def default_location(self, thing):
        "Agents start in either location at random."
        return random.choice([loc_A, loc_B])


loc_A, loc_B, loc_C = (0, 0), (1, 0), (2,0)  # The three locations for the Vacuum world

def RandomAgentProgram(actions):
    "An agent that chooses an action at random, ignoring all percepts."
    return lambda percept: random.choice(actions)
    
def RandomVacuumAgent():
    "Randomly choose one of the actions from the vacuum environment."
    return Agent(RandomAgentProgram(['Right', 'Left', 'Suck', 'NoOp']))

def ReflexVacuumAgent():
    "A reflex agent for the two-state vacuum environment. [Figure 2.8]"
    def program(percept):
        location, status = percept
        if status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return random.choice(['Left', 'Right'])
        elif location == loc_C:
            return 'Left'
    return Agent(program)
    
def ModelBasedVacuumAgent():
    "An agent that keeps track of what locations are clean or dirty."
    model = {loc_A: None, loc_B: None, loc_C: None}

    def program(percept):
        "Same as ReflexVacuumAgent, except if everything is clean, do NoOp."
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == model[loc_C] == 'Clean':
          return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        else:
          if location == loc_A:
            return 'Right'
          elif location == loc_C:
            return 'Left'
          else:
            return random.choice(['Left', 'Right'])
    return Agent(program)
    
def test_agent_inits(AgentFactory, steps, agent_type, performance_measure_type = 'default'):
    performance_measure = 0
    performance_list = []
    for loc_a_status in ['Clean', 'Dirty']:
        for loc_b_status in ['Clean', 'Dirty']:
          for loc_c_status in ['Clean', 'Dirty']:
            for default_loc in [loc_A, loc_B, loc_C]:
              agent = AgentFactory()
              env = TrivialVacuumEnvironment(performance_measure_type)
              env.status[loc_A] = loc_a_status
              env.status[loc_B] = loc_b_status
              env.status[loc_C] = loc_c_status
              env.add_thing(agent, default_loc)
              env.run(steps)
              performance_measure += agent.performance
              performance_list.append(agent.performance)
    print ("Average performance measure = {}\n".format( performance_measure/24))
    print("Full list of records:")
    print(performance_list)

test_agent_inits(ReflexVacuumAgent, 1000, 'Reflexive')
