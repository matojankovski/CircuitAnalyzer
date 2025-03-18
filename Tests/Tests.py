import pytest

from Components.BasicComponent import BasicComponent, Resistor, VoltageSource
from Components.Netlist import Circuit


@pytest.fixture
def test_circuit():
    return Circuit("Test Circuit")

@pytest.fixture
def test_voltage_source():
    return VoltageSource("V1", "1", "0", "10")

@pytest.fixture
def test_resistor_1():
    return Resistor("R1", "1", "2", "1k")

def test_basic_component_valid_nodes(test_resistor_1):
    assert test_resistor_1.component_name == "R1"
    assert test_resistor_1.netlist_1 == 1
    assert test_resistor_1.netlist_2 == 2
    assert test_resistor_1.value == 1000

def test_basic_component_invalid_nodes():
    with pytest.raises(ValueError) as excinfo:
        BasicComponent("R1", "1", "1", "100")
    assert "Invalid component connection: netlist_1 (1) and netlist_2 (1) must be different." in str(excinfo.value)

def test_duplicate_component_warning(test_circuit):
    test_circuit.add_component("R1", "1", "2", "100")
    with pytest.warns(UserWarning, match="Warning: Duplicate component name detected: R1"):
        test_circuit.add_component("R1", "2", "0", "200")

def test_validate_nodes(test_circuit):
    test_circuit.add_component("V1", "1", "0", "100")
    test_circuit.add_component("R1", "1", "2", "100")
    test_circuit.add_component("R2", "0", "2", "100")
    test_circuit.add_component("V1", "3", "0", "100")
    invalid_nodes = [3]
    with pytest.raises(ValueError) as excinfo:
        test_circuit.validate_nodes()
    assert f"Error: Node no. {invalid_nodes} appears only once" in str(excinfo.value)
