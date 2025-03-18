import numpy as np
import pytest
from scipy.sparse import csr_matrix

from Components.BasicComponent import BasicComponent, Resistor, VoltageSource
from Components.Netlist import Circuit


@pytest.fixture
def test_circuit1():
    return Circuit("Test Circuit")

@pytest.fixture
def test_voltage_source():
    return VoltageSource("V1", "1", "0", "10")

@pytest.fixture
def test_resistor_1():
    return Resistor("R1", "1", "2", "1k")

@pytest.fixture
def test_circuit_2():
    TS2= Circuit("Test Circuit #2")
    TS2.add_component("V1", "1", "0", "10")
    TS2.add_component("R1", "1", "2", "1k")
    TS2.add_component("R2", "0", "2", "1k")
    return  TS2


def test_basic_component_valid_nodes(test_resistor_1):
    assert test_resistor_1.component_name == "R1"
    assert test_resistor_1.netlist_1 == 1
    assert test_resistor_1.netlist_2 == 2
    assert test_resistor_1.value == 1000

def test_basic_component_invalid_nodes():
    with pytest.raises(ValueError) as excinfo:
        BasicComponent("R1", "1", "1", "100")
    assert "Invalid component connection: netlist_1 (1) and netlist_2 (1) must be different." in str(excinfo.value)

def test_duplicate_component_warning(test_circuit1):
    test_circuit1.add_component("R1", "1", "2", "100")
    with pytest.warns(UserWarning, match="Warning: Duplicate component name detected: R1"):
        test_circuit1.add_component("R1", "2", "0", "200")

def test_validate_nodes(test_circuit1):
    test_circuit1.add_component("V1", "1", "0", "100")
    test_circuit1.add_component("R1", "1", "2", "100")
    test_circuit1.add_component("R2", "0", "2", "100")
    test_circuit1.add_component("V1", "3", "0", "100")
    invalid_nodes = [3]
    with pytest.raises(ValueError) as excinfo:
        test_circuit1.validate_nodes()
    assert f"Error: Node no. {invalid_nodes} appears only once" in str(excinfo.value)

# def test_G_matrix(test_circuit_2):
#     test_circuit_2.create_G_matrix()
#     expected_data = [0.001, 0.001, -0.001, -0.001, 0.001]
#     expected_row = [0, 1, 0, 1, 1]
#     expected_col = [0, 1, 1, 0, 1]
#     expected_G_matrix = csr_matrix((expected_data, (expected_row, expected_col)))
#     # print(test_circuit2.G_matrix)
#     assert test_circuit_2.G_matrix == expected_G_matrix

