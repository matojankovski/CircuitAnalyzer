from Components.BasicComponent import*
from Components.Netlist import*

if __name__ == '__main__':
    my_circuit = Circuit("New Circle")
    my_circuit.V("V1", 1, 0, 5)
    my_circuit.R("R1", 1, 2, 200)
    my_circuit.R("R2", 2, 0, 100)
    print(my_circuit)
