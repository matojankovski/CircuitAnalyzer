from Components.Netlist import Circuit

def read_file(filename):
    file = ""
    with open(filename) as f:
        for line in f:
            file += "".join(line)
    return file

def parse_file(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']
    my_circuit = Circuit("New Circle")
    for line in filename.splitlines():
        line = line.strip()
        # ignore empty lines
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
        except ValueError as ex:
            raise ValueError(f"Error parsing line {line} Value error: {ex}")

    return my_circuit
