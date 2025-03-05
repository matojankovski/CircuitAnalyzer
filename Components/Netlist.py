from Components.BasicComponent import*
from scipy.sparse import csr_matrix
import numpy as np

class Circuit:

    def __init__(self, title, ground=0):

        self.title = str(title)
        self.ground = ground
        self.ground_name = 0
        self.components= []

    def add_component_internal(self, component: BasicComponent):
        """Add a component to the circuit."""
        index = len(self.components)
        for i in range(len(self.components)):
            if component.component_name < self.components[i].component_name:
                index = i
                break

        self.components.insert(index, component)

    def add_component(self, name: str, node1, node2, value):
        if name.lower().startswith("v"):
            self.add_component_internal(VoltageSource(name, node1, node2, value))
        elif name.lower().startswith("r"):
            self.add_component_internal(Resistor(name, node1, node2, value))
        elif name.lower().startswith("c"):
            self.add_component_internal(Capacitor(name, node1, node2, value))
        elif name.lower().startswith("l"):
            self.add_component_internal(Inductor(name, node1, node2, value))

    def max_nodes(self):
        max_node_no = 0
        for component in self.components:
            max_node_no = max(max_node_no, max(component.netlist_1, component.netlist_2))

        return max_node_no

    def get_no_of_sources(self, source: str):
        no_of_sources = 0
        for component in self.components:
            if component.component_name.startswith(f"{source}"):
                no_of_sources += 1
        return no_of_sources

    def create_A_matrix(self):

        A = []
        A_row = []
        A_column = []
        max_nodes = self.max_nodes()

        for component in self.components:
            if component.component_name.startswith("R"):
                Node1, Node2 = component.netlist_1, component.netlist_2
                value = component.value

                if Node1 == 0 or Node2 == 0: #grounded
                    A.append(1.0/value)
                    A_row.append(max([Node1, Node2]) - 1)
                    A_column.append(max([Node1, Node2]) - 1)

                else: #not grounded
                    #diagolnal
                    A.append(1.0/ value)
                    A_row.append(Node1 - 1)
                    A_column.append(Node1 - 1)

                    #diagolnal
                    A.append(1.0 / value)
                    A_row.append(Node2 - 1)
                    A_column.append(Node2 - 1)

                    # Node1-Node2 term
                    A.append(-1.0 / value)
                    A_row.append(Node1 - 1)
                    A_column.append(Node2 - 1)

                    # Node2-Node1 term
                    A.append(-1.0 / value)
                    A_row.append(Node2 - 1)
                    A_column.append(Node1 - 1)

        k = 0
        # number_of_voltage_sources = self.get_no_of_sources("V")
        # while k != number_of_voltage_sources:
        for component in self.components:
            if component.component_name.startswith("V"):
                Node1, Node2 = component.netlist_1, component.netlist_2

                if Node1 == 0:  # if grounded to N1 ...
                    # negative terminal
                    A.append(-1)
                    A_row.append(Node2 - 1)
                    A_column.append(max_nodes + k)

                    # negative terminal
                    A.append(-1)
                    A_row.append(max_nodes + k)
                    A_column.append(Node2 - 1)

                    k += 1

                elif Node2 == 0:  # if grounded to N2 ...
                    # positive terminal
                    A.append(1)
                    A_row.append(Node1 - 1)
                    A_column.append(max_nodes+ k)

                    # positive terminal
                    A.append(1)
                    A_row.append(max_nodes + k)
                    A_column.append(Node1 - 1)

                    k += 1

                else:  # if not grounded ...
                    # positive terminal
                    A.append(1)
                    A_row.append(Node1 - 1)
                    A_column.append(max_nodes + k)

                    # positive terminal
                    A.append(1)
                    A_row.append(max_nodes + k)
                    A_column.append(Node1 - 1)

                    # negative terminal
                    A.append(-1)
                    A_row.append(Node2 - 1)
                    A_column.append(max_nodes+ k)

                    # negative terminal
                    A.append(-1)
                    A_row.append(max_nodes+ k)
                    A_column.append(Node2 - 1)

                    k += 1

        self.A = csr_matrix((A, (A_row, A_column)))
        return self.A

    def create_z_matrix(self):
        """
        'rhs_matrix' creates the right hand side matrix

        :return: rhs, right hand side
        """
        # initialize rhs
        max_nodes = self.max_nodes()
        number_of_voltage_sources = self.get_no_of_sources("V")
        number_of_current_sources = self.get_no_of_sources("I")
        z_matrix = [0] * (max_nodes + number_of_voltage_sources + number_of_current_sources)
        k = 0
        for component in self.components:
            if component.component_name.startswith("V"):
                z_matrix[max_nodes + k] += component.value
                k += 1

        self.z_matrix = np.array(z_matrix)
        return self.z_matrix









