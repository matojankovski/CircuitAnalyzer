from scipy.sparse.linalg import spsolve

from Components.Netlist import Circuit


def read_netlist(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']
    operation = ""

    my_circuit = Circuit("New Circle")
    with open(filename) as f:
        for line in f:
            if line[0].upper() in components_nomenaclature:
                component_name, netlist_1, netlist_2, value= line.split()
                my_circuit.add_component(component_name, netlist_1, netlist_2, value)

            if line.startswith(".op"):
                A = my_circuit.create_A_matrix()
                z = my_circuit.create_z_matrix()
                solution = spsolve(A, z)
                i = my_circuit.incidence_matrix()
                my_circuit.get_OP(solution, i)

    # return my_circuit






