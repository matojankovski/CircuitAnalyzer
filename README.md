Simple CircuitAnalyzer 

Circuit Analyzer is based on SPICE. It incorporates Modified Nodal Analaysis (MNA). Any circuit can be represented by sets of equations. 
The common methods to create these sets of equations are the node voltage method and the loop-current method. MNA allows easier algorithmic
solution.

MNA steps
  1. Reference node, usually ground. N-1 remaining nodes
  2. Assignment of the current through each voltage source
  3. Application of Kirchoff current law to each node
  4. Equation for voltage of each voltage source
  5. Solving of the system of n-1 unknowns

Example Circuit:
V1 1 0 32
R1 1 2 2k
R2 2 3 4k
R3 2 0 8k
V2 3 0 20

![Screenshot from 2025-03-16 22-24-49](https://github.com/user-attachments/assets/12ec8f1c-fd6c-492f-8b7a-2108bfb24ebd)



