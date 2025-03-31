import numpy as np
import pytest
from scipy.sparse import csr_matrix
from Components.Solver import read_file  # Replace with the actual module name

from Components.BasicComponent import BasicComponent, Resistor, VoltageSource, CurrentSource
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
def test_current_source():
    return CurrentSource("I1", "1", "2", "1k")

@pytest.fixture
def test_circuit_2():
    TS2= Circuit("Test Circuit #2")
    TS2.add_component("V1", "1", "0", "10")
    TS2.add_component("R1", "1", "2", "1k")
    TS2.add_component("R2", "0", "2", "1k")
    return TS2

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

def test_incorrect_value(test_circuit1):
    with pytest.raises(ValueError, match=r"Invalid value for R1: -200\.0\. Value cannot be negative\."):
        test_circuit1.add_component("R1", "1", "0", "-200")

def test_convert_unit_micro():
    test_resistor1 = Resistor("R1", "1", "2", "2.2u")
    assert test_resistor1.value == 2.2e-6

def test_validate_nodes(test_circuit1):
    test_circuit1.add_component("V1", "1", "0", "100")
    test_circuit1.add_component("R1", "1", "2", "100")
    test_circuit1.add_component("R2", "0", "2", "100")
    test_circuit1.add_component("V1", "3", "0", "100")
    invalid_nodes = [3]
    with pytest.raises(ValueError) as excinfo:
        test_circuit1.validate_nodes()
    assert f"Error: Node no. {invalid_nodes} appears only once" in str(excinfo.value)

def test_resistor_in_circuit(test_circuit1):
    test_circuit1.add_component("R1", "1", "2", "5k")
    assert any(isinstance(c, Resistor) and c.component_name == "R1" for c in test_circuit1.components)

def test_voltage_source_in_circuit(test_circuit1):
    test_circuit1.add_component("V1", "1", "2", "5")
    assert any(isinstance(c, VoltageSource) and c.component_name == "V1" for c in test_circuit1.components)

def test_current_source_in_circuit(test_circuit1):
    test_circuit1.add_component("I1", "1", "0", "0.005")
    assert any(isinstance(c, CurrentSource) and c.component_name == "I1" for c in test_circuit1.components)

def test_G_matrix(test_circuit_2):
    G, G_row, G_collumn = test_circuit_2.create_G_matrix()
    expected_data = [0.001, 0.001, -0.001, -0.001, 0.001]
    expected_row = [0, 1, 0, 1, 1]
    expected_col = [0, 1, 1, 0, 1]
    assert (G, G_row, G_collumn) == (expected_data, expected_row, expected_col)

def test_B_matrix(test_circuit_2):
    B, B_row, B_collumn = test_circuit_2.create_B_matrix()
    expected_data = [1]
    expected_row = [0]
    expected_col = [0]
    assert (B, B_row, B_collumn) == (expected_data, expected_row, expected_col)

def test_read_file(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("V1 1 0 10\nR2 1 2 10k\nR1 2 0 10k\nV2 2 0 20\n.op")
    result = read_file(test_file)
    assert result == "V1 1 0 10\nR2 1 2 10k\nR1 2 0 10k\nV2 2 0 20\n.op"