from Components.Netlist import Circuit
from scipy.sparse.linalg import spsolve

def solve_circuit(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']

    my_circuit = Circuit("New Circle")
    with open(filename) as f:
        for line in f:
            line = line.strip()
            #ignore empty lines
            if not line or line.startswith("*"):
                continue

            if line.startswith(".op"):
                my_circuit.operation = "DC"
                continue

            if line[0].upper() not in components_nomenaclature:
                raise ValueError(f"Invalid component name in line: {line}")

            try:
                component_name, netlist_1, netlist_2, value = line.split()
                my_circuit.add_component(component_name, netlist_1, netlist_2, value)
            except ValueError:
                raise ValueError(f"Error parsing line: {line}")

        my_circuit.validate_nodes()
        my_circuit.solvematrix()



