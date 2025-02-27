from Components.BasicComponent import*
from scipy.sparse import csr_matrix
import numpy as np

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

    def max_nodes(self):
        max_node_no = 0
        for component in self.components:
            max_node_no = max(max_node_no, max(component.netlist_1, component.netlist_2))

        return max_node_no


    def create_conductance_matrix(self):

        g = []
        g_row = []
        g_column = []
        max_nodes = self.max_nodes()

        for component in self.components:
            if component.component_name.startswith("R"):
                Node1, Node2 = component.netlist_1, component.netlist_2

                if Node1 == 0 or Node2 == 0: #grounded
                    g.append(1.0/component.value)
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

        for k, component in enumerate(self.components):
            if component.component_name.startswith("V"):
                Node1, Node2 = component.netlist_1, component.netlist_2


                if Node1 == 0:  # if grounded to N1 ...
                    # negative terminal
                    g.append(-1)
                    g_row.append(Node2 - 1)
                    g_column.append(max_nodes + k)

                    # negative terminal
                    g.append(-1)
                    g_row.append(max_nodes + k)
                    g_column.append(Node2 - 1)

                elif Node2 == 0:  # if grounded to N2 ...
                    # positive terminal
                    g.append(1)
                    g_row.append(Node1 - 1)
                    g_column.append(max_nodes+ k)

                    # positive terminal
                    g.append(1)
                    g_row.append(max_nodes + k)
                    g_column.append(Node1 - 1)

                else:  # if not grounded ...
                    # positive terminal
                    g.append(1)
                    g_row.append(Node1 - 1)
                    g_column.append(max_nodes + k)

                    # positive terminal
                    g.append(1)
                    g_row.append(max_nodes + k)
                    g_column.append(Node1 - 1)

                    # negative terminal
                    g.append(-1)
                    g_row.append(Node2 - 1)
                    g_column.append(max_nodes+ k)

                    # negative terminal
                    g.append(-1)
                    g_row.append(max_nodes+ k)
                    g_column.append(Node2 - 1)






        self.G = csr_matrix((g,(g_row,g_column)))
        return self.G











