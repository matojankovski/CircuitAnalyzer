from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix, bmat
import numpy as np
import warnings

from Components.BasicComponent import *


class Circuit:

    def __init__(self, title, ground=0):

        self.title = str(title)
        self.ground = ground
        self.components = []
        self.operation = None

        self.G_matrix = None
        self.A_matrix = None
        self.B_matrix = None
        self.C_matrix = None
        self.D_matrix = None
        self.z_matrix = None
        self.x_matrix = None

        self.max_n = None

    def add_component_internal(self, component: BasicComponent):
        existing_names = {comp.component_name for comp in self.components}
        if component.component_name in existing_names:
            warnings.warn(f"Warning: Duplicate component name detected: {component.component_name}")

        # add component in-place-sorted
        index = len(self.components)
        for i in range(len(self.components)):
            if component.component_name < self.components[i].component_name:
                index = i
                break
        self.components.insert(index, component)

    def add_component(self, name: str, node1, node2, value):
        # add component according to the nomenclature
        if name.lower().startswith("v"):
            self.add_component_internal(VoltageSource(name, node1, node2, value))
        elif name.lower().startswith("r"):
            self.add_component_internal(Resistor(name, node1, node2, value))
        elif name.lower().startswith("c"):
            self.add_component_internal(Capacitor(name, node1, node2, value))
        elif name.lower().startswith("l"):
            self.add_component_internal(Inductor(name, node1, node2, value))
        elif name.lower().startswith("i"):
            self.add_component_internal(CurrentSource(name, node1, node2, value))

    def validate_nodes(self):
        node_counts = {}
        for component in self.components:
            if component.netlist_1 not in node_counts:
                node_counts[component.netlist_1] = 0
            if component.netlist_2 not in node_counts:
                node_counts[component.netlist_2] = 0
            node_counts[component.netlist_1] += 1
            node_counts[component.netlist_2] += 1

        invalid_nodes = []
        for node, count in node_counts.items():
            if count == 1 and node != self.ground:
                invalid_nodes.append(node)
        if invalid_nodes:
            raise ValueError(f"Error: Node no. {invalid_nodes} appears only once")

        return None

    def max_nodes(self):
        if self.max_n:
            return self.max_n

        max_node_no = 0
        for component in self.components:
            max_node_no = max(max_node_no, max(component.netlist_1, component.netlist_2))

        self.max_n = max_node_no
        return max_node_no

    def get_no_of_sources(self, source: str):
        no_of_sources = 0
        for component in self.components:
            if component.component_name.startswith(f"{source}"):
                no_of_sources += 1
        return no_of_sources

    def create_G_matrix(self):
        # creates A matrix in equation Ax=z
        # has only passive elements
        # elements connected to ground appear only on the diagonal
        # elements not connected to ground are both on the diagonal and off-diagonal terms
        G = []
        G_row = []
        G_column = []

        for component in self.components:
            if component.component_name.startswith("R"):
                Node1, Node2 = component.netlist_1, component.netlist_2
                value = component.value

                # connection to ground
                if Node1 == 0 or Node2 == 0:
                    G.append(1.0 / value)
                    G_row.append(max([Node1, Node2]) - 1)
                    G_column.append(max([Node1, Node2]) - 1)
                # not grounded
                else:
                    # diagolnal
                    G.append(1.0 / value)
                    G_row.append(Node1 - 1)
                    G_column.append(Node1 - 1)

                    # diagolnal
                    G.append(1.0 / value)
                    G_row.append(Node2 - 1)
                    G_column.append(Node2 - 1)

                    # Node1-Node2 term
                    G.append(-1.0 / value)
                    G_row.append(Node1 - 1)
                    G_column.append(Node2 - 1)

                    # Node2-Node1 term
                    G.append(-1.0 / value)
                    G_row.append(Node2 - 1)
                    G_column.append(Node1 - 1)

        return G, G_row, G_column

    def create_CSR_G_matrix(self):
        G, G_row, G_column = self.create_G_matrix()
        self.G_matrix = csr_matrix((G, (G_row, G_column)))
        # print(f"G matrix is {self.G_matrix}")

    def create_B_matrix(self):
        B = []
        B_row = []
        B_column = []

        n = 0
        for component in self.components:
            if component.component_name.startswith("V"):
                Node1, Node2 = component.netlist_1, component.netlist_2

                #  Node1 is grounded, add Node2
                if Node1 == 0:
                    B.append(1)
                    B_row.append(Node2 - 1)  # Node index
                    B_column.append(n)  # voltage source index

                #  Node2 is grounded, add Node1
                elif Node2 == 0:
                    B.append(1)
                    B_row.append(Node1 - 1)  # Node index
                    B_column.append(n)  # voltage source index

                # VS is not grounded
                else:
                    # Positive terminal (Node1)
                    B.append(1)
                    B_row.append(Node1 - 1)
                    B_column.append(n)

                    # Negative terminal (Node2)
                    B.append(-1)
                    B_row.append(Node2 - 1)
                    B_column.append(n)

                n += 1
        return B, B_row, B_column

    def create_CSR_B_matrix(self):
        max_node_no = self.max_nodes()
        number_of_voltage_sources = self.get_no_of_sources("V")
        B, B_row, B_column = self.create_B_matrix()
        self.B_matrix = csr_matrix((B, (B_row, B_column)), shape=(max_node_no, number_of_voltage_sources))
        # print(f"B matrix is {self.B_matrix}")

    def create_CSR_C_matrix(self):
        self.C_matrix = self.B_matrix.transpose()
        # print(f"C matrix is {self.C_matrix}")

    def create_CSR_D_matrix(self):
        number_of_voltage_sources = self.get_no_of_sources("V")
        self.D_matrix = csr_matrix((number_of_voltage_sources, number_of_voltage_sources))
        # print(f"D matrix is {self.D_matrix}")
        # return self.D_matrix

    def create_A_matrix(self):
        self.create_CSR_G_matrix()
        self.create_CSR_B_matrix()
        self.create_CSR_C_matrix()
        self.create_CSR_D_matrix()
        # print("G shape:", self.G_matrix.shape)
        # print("B shape:", self.B_matrix.shape)
        # print("C shape:", self.C_matrix.shape)
        # print("D shape:", self.D_matrix.shape)

        self.A_matrix = bmat([[self.G_matrix, self.B_matrix], [self.C_matrix, self.D_matrix]], format="csr")
        # print(f"A matrix is :{self.A_matrix}")

    def create_z_matrix(self):
        #contains know voltage/current sources
        max_nodes = self.max_nodes()
        number_of_voltage_sources = self.get_no_of_sources("V")
        number_of_current_sources = self.get_no_of_sources("I")
        z_matrix = [0] * (max_nodes + number_of_voltage_sources)
        k = 0
        for component in self.components:
            if component.component_name.startswith("V"):
                z_matrix[max_nodes + k] += component.value
                k += 1
            if component.component_name.startswith("I"):
                Node1, Node2 = component.netlist_1, component.netlist_2
                if Node1 == 0:
                    z_matrix[Node2 - 1] += component.value

                elif Node2 == 0:
                    z_matrix[Node1 - 1] += component.value

                else:
                    z_matrix[Node1 - 1] -= component.value
                    z_matrix[Node2 - 1] += component.value

        self.z_matrix = np.array(z_matrix)
        # print(f" z_matrix/RHS is {self.z_matrix}")
        # return z_matrix

    def solvematrix(self):
        self.create_z_matrix()
        self.create_A_matrix()
        self.x_matrix = spsolve(self.A_matrix, self.z_matrix)
        # self.get_resistor_voltage()

    def get_voltage_current(self, component, k=0):
        # for component in self.components:
        number_of_voltage_sources = self.get_no_of_sources("V")
        number_of_current_sources = self.get_no_of_sources("I")
        if component.component_name.startswith("R"):
            Node1, Node2 = component.netlist_1, component.netlist_2

            V_n1 = self.x_matrix[Node1 - 1] if Node1 != 0 else 0
            V_n2 = self.x_matrix[Node2 - 1] if Node2 != 0 else 0
            V_R = V_n1 - V_n2
            I_R = V_R / component.value
            # print(f"Voltage on {component.component_name} is {V_R}, current: {I_R}")
            return V_R, I_R
        elif component.component_name.startswith("V"):
            num_nodes = self.max_nodes()
            V_V = component.value
            I_V = self.x_matrix[num_nodes + k]
            # print(f"Voltage on {component.component_name} is {V_V}, current: {I_V}")
            return V_V, I_V
        elif component.component_name.startswith("I"):
            Node1, Node2 = component.netlist_1, component.netlist_2
            V_n1 = self.x_matrix[Node1 - 1] if Node1 != 0 else 0
            V_n2 = self.x_matrix[Node2 - 1] if Node2 != 0 else 0
            V_I  = V_n1 - V_n2
            I_I = component.value
            # print(f"Voltage on {component.component_name} is {V_I}, current: {I_I}")
            return V_I, I_I
        return None

    def get_OP(self):
        result = ""
        k = 0
        for component in self.components:
            result += f"{component.component_name}\n"
            if component.component_name.startswith("R"):
                V_R, I_R = self.get_voltage_current(component)
                result += f"{'Voltage:':<10}{('{:.3f}'.format(V_R).rstrip('0').rstrip('.')):>10} V\n"
                result += f"{'Current:':<10}{('{:.3f}'.format(I_R).rstrip('0').rstrip('.')):>10} A\n"
                result += f"{'Power:':<10}{('{:.3f}'.format(V_R * I_R).rstrip('0').rstrip('.')):>10} W\n"

            if component.component_name.startswith("V"):
                V_V, I_V = self.get_voltage_current(component, k)
                result += f"{'Voltage:':<10}{('{:.3f}'.format(V_V).rstrip('0').rstrip('.')):>10} V\n"
                result += f"{'Current:':<10}{('{:.5f}'.format(I_V).rstrip('0').rstrip('.')):>10} A\n"
                result += f"{'Power:':<10}{('{:.3f}'.format(V_V * I_V).rstrip('0').rstrip('.')):>10} W\n"
                k += 1

            if component.component_name.startswith("I"):
                V_I, I_I = self.get_voltage_current(component, k)
                result += f"{'Voltage:':<10}{('{:.3f}'.format(V_I).rstrip('0').rstrip('.')):>10} V\n"
                result += f"{'Current:':<10}{('{:.5f}'.format(I_I).rstrip('0').rstrip('.')):>10} A\n"
                result += f"{'Power:':<10}{('{:.3f}'.format(V_I * I_I).rstrip('0').rstrip('.')):>10} W\n"

        print(result)
        # return result
