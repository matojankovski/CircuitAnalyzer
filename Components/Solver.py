from Components.Netlist import Circuit


def read_netlist(filename):
    components_nomenaclature = ['V', 'I', 'R', 'C', 'L', 'E', 'F', 'G', 'H']


    my_circuit = Circuit("New Circle")
    with open(filename) as f:
        for b, line in enumerate(f):
            if line[0].upper() in components_nomenaclature:
                component_name, netlist_1, netlist_2, value= line.split()
                my_circuit.add_component(component_name, netlist_1, netlist_2, value)

    return my_circuit





