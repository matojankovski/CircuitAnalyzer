import unittest
import pytest
from Components.BasicComponent import Resistor, BasicComponent


class MyTestCase(unittest.TestCase):

    def test_basic_component_valid_nodes(self):
        component = BasicComponent("R1", "1", "2", "100")
        assert component.netlist_1 == 1
        assert component.netlist_2 == 2
        assert component.value == 100.0

    def test_basic_component_invalid_nodes(self):
        with pytest.raises(ValueError) as excinfo:
            BasicComponent("R1", "1", "1", "100")
        assert "Invalid component connection: netlist_1 (1) and netlist_2 (1) must be different." in str(excinfo.value)

    def test_basic_component_invalid_nodes_different_types(self):
        with pytest.raises(ValueError) as excinfo:
            BasicComponent("R1", 1, 1, 100)
        assert "Invalid component connection: netlist_1 (1) and netlist_2 (1) must be different." in str(excinfo.value)


if __name__ == '__main__':
    unittest.main()

