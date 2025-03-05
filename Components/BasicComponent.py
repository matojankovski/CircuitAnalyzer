class BasicComponent:
    unit = ""  # Default unit (empty)
    unit_prefix = {'meg': 'e6', 'f': 'e-15', 'p': 'e-12', 'n': 'e-9', 'u': 'e-6', 'm': 'e-3', 'k': 'e3', 'g': 'e9',
                        't': 'e12'}

    def __init__(self, component_name, netlist_1, netlist_2, value):
        self.component_name = str(component_name)
        self.netlist_1 = int(netlist_1)
        self.netlist_2 = int(netlist_2)
        self.value = float(self.convert_unit(value))

    def __str__(self):
        return f"{self.component_name} {self.netlist_1} {self.netlist_2} {self.value} {self.unit}"

    def __repr__(self):
        return f"BasicComponent(\'{self.component_name}, {self.netlist_1}, {self.netlist_2}, {self.value} {self.unit})"

    def convert_unit(self, string):
        for prefix, prefix_value in self.unit_prefix.items():
            if prefix in string:
                string = string.replace(prefix, prefix_value)
                break

        return string


class Resistor(BasicComponent):
    unit = "Ω"  # Define unit for resistors

class Capacitor(BasicComponent):
    unit = "F"  # Define unit for capacitors

class Inductor(BasicComponent):
    unit = "H"  # Henrys

class VoltageSource(BasicComponent):
    unit = "V" #Volts

