from scipy.sparse.linalg import spsolve

from Components.BasicComponent import*
from Components.Netlist import*
from Components.Solver import read_netlist

if __name__ == '__main__':
    read_netlist("TestCircuit1.cir")
