from Components.Netlist import Circuit
from scipy.sparse.linalg import spsolve

def read_netlist(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']

    my_circuit = Circuit("New Circle")
    with open(filename) as f:
        for line in f:
            if line[0].upper() in components_nomenaclature:
                component_name, netlist_1, netlist_2, value= line.split()
                my_circuit.add_component(component_name, netlist_1, netlist_2, value)

            if line.startswith(".op"):
                A_matrix = my_circuit.create_Z_matrix()
                B_matrix = my_circuit.create_B_matrix()
                C_matrix = my_circuit.create_C_matrix()
                D_matrix = my_circuit.create_d_matrix()
                A_matrix = my_circuit.create_A_matrix()
                z_matrix = my_circuit.create_z_matrix()
                x_matrix = spsolve(A_matrix, z_matrix)
                i = my_circuit.incidence_matrix()
                print(my_circuit.get_OP(x_matrix, i))


