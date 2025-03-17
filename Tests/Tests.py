# import unittest
import pytest
from Components.BasicComponent import Resistor, BasicComponent
from Components.Netlist import Circuit


# class MyTestCase(unittest.TestCase):

@pytest.fixture
def circuit():
    """Fixture to create a new Circuit instance for tests."""
    return Circuit("Test Circuit")

def test_basic_component_valid_nodes(self):
    component = BasicComponent("R1", "1", "2", "100")
    assert component.component_name == "R1"
    assert component.netlist_1 == 1
    assert component.netlist_2 == 2
    assert component.value == 100.0

def test_basic_component_invalid_nodes(self):
    with pytest.raises(ValueError) as excinfo:
        BasicComponent("R1", "1", "1", "100")
    assert "Invalid component connection: netlist_1 (1) and netlist_2 (1) must be different." in str(excinfo.value)

def test_duplicate_component_warning(self, circuit):
    # circuit = Circuit("Test Circuit")
    circuit.add_component("R1", "1", "2", "100")
    with pytest.warns(UserWarning, match="Warning: Duplicate component name detected: R1"):
        circuit.add_component("R1", "2", "0", "200")

def test_validate_nodes(self, circuit):
    circuit.add_component("V1", "1", "0", "100")
    circuit.add_component("R1", "1", "2", "100")
    circuit.add_component("R2", "0", "2", "100")
    circuit.add_component("V1", "3", "0", "100")
    invalid_nodes = [3]
    with pytest.raises(ValueError) as excinfo:
        circuit.validate_nodes()
    assert f"Error: Node no. {invalid_nodes} appears only once" in str(excinfo.value)



# if __name__ == '__main__':
#     unittest.main()

