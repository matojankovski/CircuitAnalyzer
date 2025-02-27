from Components.BasicComponent import*

class Circuit:

    def __init__(self, title, ground=0):

        self.title = str(title)
        self.ground = ground
        self.ground_name = 0
        self.components= []

    def add_component(self, component):
        """Add a component to the circuit."""
        self.components.append(component)

    @property
    def R(self):
        return lambda name, node1, node2, value: self.add_component(Resistor(name, node1, node2, value))

    @property
    def C(self):
        return lambda name, node1, node2, value: self.add_component(Capacitor(name, node1, node2, value))

    @property
    def V(self):
        return lambda name, node1, node2, value: self.add_component(VoltageSource(name, node1, node2, value))


    def create_conductance_matrix(self):

        g = []
        g_row = []
        g_column = []

        for component in self.components:
            if component.component_name.startswith("R"):
                Node1, Node2 = component.netlist_1, component.netlist_2

                if Node1 == 0 or Node2 == 0: #grounded
                    g.append(1/0/component.value)
                    g_row.append(max([Node1, Node2]) - 1)
                    g_column.append(max([Node1, Node2]) - 1)

                else: #not grounded
                    #diagolnal
                    g.append(1.0/ component.value)
                    g_row.append(Node1 - 1)
                    g_column.append(Node1 - 1)

                    #diagolnal
                    g.append(1.0 / component.value)
                    g_row.append(Node2 - 1)
                    g_column.append(Node2 - 1)

                    # Node1-Node2 term
                    g.append(-1.0 / component.value)
                    g_row.append(Node1 - 1)
                    g_column.append(Node2 - 1)

                    # Node2-Node1 term
                    g.append(-1.0 / component.value)
                    g_row.append(Node2 - 1)
                    g_column.append(Node1 - 1)








