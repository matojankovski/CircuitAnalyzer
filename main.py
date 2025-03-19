import sys

from Components.Solver import parse_file, read_file
from Components.Netlist import Circuit


if __name__ == '__main__':
    if len(sys.argv) == 1:
        filename = "TestCircuit2.cir"
        print(f"Missing file. To run this program write `python main.py <filename>`")
        exit(0)
    filename = sys.argv[1]
    try:
        netlist = read_file(filename)
        circuit = parse_file(netlist)
        circuit.validate_nodes()
        circuit.solvematrix()
        circuit.get_OP()

    except ValueError as ex:
        print(f"Your input val was invalid {ex}")
    except Exception as ex:
        print(f"Unknown error {ex}")
