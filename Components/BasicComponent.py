class BasicComponent:
    unit = ""  # Default unit (empty)
    unit_prefix = {'meg': 'e6', 'f': 'e-15', 'p': 'e-12', 'n': 'e-9', 'u': 'e-6', 'm': 'e-3', 'k': 'e3', 'g': 'e9',
                        't': 'e12'}
    component_prefix = ["R", "V", "I"]

    def __init__(self, component_name, netlist_1, netlist_2, value):
        self.component_name = str(component_name)
        self.netlist_1 = int(netlist_1)
        self.netlist_2 = int(netlist_2)
        self.value = float(self.convert_unit(value))

        if self.value < 0 and isinstance(self, Resistor):
            raise ValueError(f"Invalid value for {self.component_name}: {self.value}. Value cannot be negative.")

            # ensure that nodes have different numbers
        if self.netlist_1 == self.netlist_2:
            raise ValueError(
                f"Invalid component connection: netlist_1 ({netlist_1}) and netlist_2 ({netlist_2}) must be different.")
        if not component_name.startswith(tuple(self.component_prefix)):
            raise ValueError(f"Invalid value component name.")

    def __str__(self):
        return (
            f"Component: {self.component_name}, "
            f"Nodes: ({self.netlist_1}, {self.netlist_2}), "
            f"Value: {self.value} {getattr(self, 'unit', '')}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"component_name={repr(self.component_name)}, "
            f"netlist_1={self.netlist_1}, "
            f"netlist_2={self.netlist_2}, "
            f"value={self.value}, "
            f"unit={repr(getattr(self, 'unit', None))})"
        )


    def convert_unit(self, string):
        #handle metric prefixes
        # try:
        #     if not isinstance(string, str):
        #         raise TypeError("Input must be string")

        for prefix, prefix_value in self.unit_prefix.items():
            if prefix in string:
                string = string.replace(prefix, prefix_value)
                break

        return string

class Resistor(BasicComponent):
    unit = "Ω"

class Capacitor(BasicComponent):
    unit = "F"

class Inductor(BasicComponent):
    unit = "H"

class VoltageSource(BasicComponent):
    unit = "V"

class CurrentSource(BasicComponent):
    unit = "A"
