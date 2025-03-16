from Components.BasicComponent import*
from scipy.sparse import csr_matrix, bmat
import numpy as np

class Circuit:

    def __init__(self, title, ground=0):

        self.title = str(title)
        self.ground = ground
        self.ground_name = 0
        self.components= []

    def add_component_internal(self, component: BasicComponent):
        #add component in-place-sorted
        index = len(self.components)
        for i in range(len(self.components)):
            if component.component_name < self.components[i].component_name:
                index = i
                break
        self.components.insert(index, component)

    def add_component(self, name: str, node1, node2, value):
        #add component according to the nomenaclature
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

    def create_Z_matrix(self):
        #creates A matrix in equation Ax=z
        #has only passive elements
        #elements connected to ground appear only on the diagonal
        #elements not connected to ground are both on the diagonal and off-diagonal terms
        Z = []
        Z_row = []
        Z_column = []

        for component in self.components:
            if component.component_name.startswith("R"):
                Node1, Node2 = component.netlist_1, component.netlist_2
                value = component.value

                # connection to ground
                if Node1 == 0 or Node2 == 0:
                    Z.append(1.0/value)
                    Z_row.append(max([Node1, Node2]) - 1)
                    Z_column.append(max([Node1, Node2]) - 1)
                # not grounded
                else:
                    #diagolnal
                    Z.append(1.0/ value)
                    Z_row.append(Node1 - 1)
                    Z_column.append(Node1 - 1)

                    #diagolnal
                    Z.append(1.0 / value)
                    Z_row.append(Node2 - 1)
                    Z_column.append(Node2 - 1)

                    # Node1-Node2 term
                    Z.append(-1.0 / value)
                    Z_row.append(Node1 - 1)
                    Z_column.append(Node2 - 1)

                    # Node2-Node1 term
                    Z.append(-1.0 / value)
                    Z_row.append(Node2 - 1)
                    Z_column.append(Node1 - 1)

        self.Z = csr_matrix((Z, (Z_row, Z_column)))
        print(self.Z)
        return Z

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
                    B_row.append(Node2 - 1)  #Node index
                    B_column.append(n)  #voltage source index

                #  Node2 is grounded, add Node1
                elif Node2 == 0:
                    B.append(1)
                    B_row.append(Node1 - 1) #Node index
                    B_column.append(n) #voltage source index

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

        self.B = csr_matrix((B, (B_row, B_column)))
        print(self.B)
        return self.B

    def create_C_matrix(self):
        self.C = self.B.transpose()
        print (self.C)
        return self.C

    def create_d_matrix(self):
        number_of_voltage_sources = self.get_no_of_sources("V")
        self.D = csr_matrix((number_of_voltage_sources, number_of_voltage_sources))
        print(self.D)
        return self.D

    def create_A_matrix(self):
        self.A = bmat([[self.Z, self.B], [self.C, self.D]], format="csr")
        print(self.A)
        return self.A

    def create_z_matrix(self):
        #right-hand-side matrix containing know voltage sources
        max_nodes = self.max_nodes()
        number_of_voltage_sources = self.get_no_of_sources("V")
        number_of_current_sources = self.get_no_of_sources("I")
        z_matrix = [0] * (max_nodes + number_of_voltage_sources + number_of_current_sources)
        k = 0
        for component in self.components:
            if component.component_name.startswith("V"):
                z_matrix[max_nodes + k] += component.value
                k += 1

        z_matrix = np.array(z_matrix)
        return z_matrix

    def incidence_matrix(self):
        a = []
        a_row = []
        a_col = []

        k = 0
        for component in self.components:
            Node1, Node2 = component.netlist_1, component.netlist_2

            #connection to ground
            if Node1 == 0:
                a.append(-1)
                a_row.append(Node2 - 1)
                a_col.append(k)
            # connection to ground
            elif Node2 == 0:
                a.append(1)
                a_row.append(Node1 - 1)
                a_col.append(k)
            else:
                a.append(1)
                a_row.append(Node1 - 1)
                a_col.append(k)
                a.append(-1)
                a_row.append(Node2 - 1)
                a_col.append(k)
            k += 1

        i_m = csr_matrix((a, (a_row, a_col)))
        return i_m

    def get_OP(self, solved_matrix, incidence_matrix):
        result = ""
        max_nodes = self.max_nodes()

        vb = incidence_matrix.transpose() * solved_matrix[:max_nodes, ...]
        k = 0
        for component in self.components:
            result += f"{component.component_name}\n"
            result += f"{'Voltage:':<10}{('{:.3f}'.format(vb[k]).rstrip('0').rstrip('.')):>10} V\n"
            if component.component_name.startswith("V"):
                result += f"{'Current:':<10}{('{:.5f}'.format(solved_matrix[k]).rstrip('0').rstrip('.')):>10} I\n"
                result += f"{'Power:':<10}{('{:.5f}'.format(vb[k] * solved_matrix[k]).rstrip('0').rstrip('.')):>10} W\n"
            else:
                result += f"{'Current:':<10}{('{:.5f}'.format(vb[k] / component.value).rstrip('0').rstrip('.')):>10} I\n"
                result += f"{'Power:':<10}{('{:.5f}'.format(vb[k] * vb[k] / component.value).rstrip('0').rstrip('.')):>10} W\n"
            k += 1
        return result















