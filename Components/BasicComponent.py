class BasicComponent:
    unit = ""  # Default unit (empty)

    def __init__(self, component_name, netlist_1, netlist_2, value):
        self.component_name = str(component_name)
        self.netlist_1 = netlist_1
        self.netlist_2 = netlist_2
        self.value = value

    def __str__(self):
        return f"{self.component_name} {self.netlist_1} {self.netlist_2} {self.value} {self.unit}"

    def __repr__(self):
        return f"BasicComponent(\'{self.component_name}, {self.netlist_1}, {self.netlist_2}, {self.value} {self.unit})"

class Resistor(BasicComponent):
    unit = "Ω"  # Define unit for resistors

class Capacitor(BasicComponent):
    unit = "F"  # Define unit for capacitors

class Inductor(BasicComponent):
    unit = "H"  # Henrys

class VoltageSource(BasicComponent):
    unit = "V" #Volts

