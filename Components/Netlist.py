from Components.BasicComponent import*

class Circuit:

    def __init__(self, title, ground=0):

        self.title = str(title)
        self.ground = ground
        self.ground_name = 0
        self.global_nodes= []

    def add_component(self, component):
        """Add a component to the circuit."""
        self.global_nodes.append(component)

    @property
    def R(self):
        return lambda name, node1, node2, value: self.add_component(Resistor(name, node1, node2, value))

    @property
    def C(self):
        return lambda name, node1, node2, value: self.add_component(Capacitor(name, node1, node2, value))

    @property
    def V(self):
        return lambda name, node1, node2, value: self.add_component(VoltageSource(name, node1, node2, value))



