from Components.Netlist import Circuit
from scipy.sparse.linalg import spsolve

def solve_circuit(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']

    my_circuit = Circuit("New Circle")
    with open(filename) as f:
        for line in f:
            # if line[0] != "*":
            try:
                if line[0].upper() in components_nomenaclature:
                    component_name, netlist_1, netlist_2, value= line.split()
                    my_circuit.add_component(component_name, netlist_1, netlist_2, value)
                elif not line.strip():
                    my_circuit.validate_nodes()
                elif line.startswith(".op"):
                    my_circuit.operation = "DC"
                else:
                    raise ValueError(f"Invalid component {line[0]}")
            except ValueError as e:
                print(f"Error adding component {e}")
                return

        my_circuit.solvematrix()



