# Simple CircuitAnalyzer 

Circuit Analyzer is based on SPICE. It incorporates Modified Nodal Analaysis (MNA). Any circuit can be represented by sets of equations. 
The common methods to create these sets of equations are the node voltage method and the loop-current method. MNA allows easier algorithmic
solution.

## MNA steps
  1. Reference node, usually ground. N-1 remaining nodes
  2. Assignment of the current through each voltage source
  3. Application of Kirchoff current law to each node
  4. Equation for voltage of each voltage source
  5. Solving of the system of n-1 unknowns

### Example Circuit:
```
V1 1 0 10
R1 1 2 1k
R2 2 3 1k
R3 2 0 2k
V2 3 0 10
```
![Screenshot from 2025-03-16 22-24-49](https://github.com/user-attachments/assets/12ec8f1c-fd6c-492f-8b7a-2108bfb24ebd)

Equations for circuit can be shown as:
  $Ax = z$

  ![Screenshot from 2025-03-17 19-41-24](https://github.com/user-attachments/assets/469d50df-b59d-41a2-bb3a-44bc4e863046)


Matrix A consists of 4 matrices, $(m+n)x(m+n)$, where n is the number of nodes, and m is the number of independent voltage sources. Generally it can be described as:

xxx

G matrix $(n × n)$ is determined by the interconnections between the passive circuit elements.
B matrix $(n × m)$ is determined by the connection of the voltage sources.
C matrix $(m × n)$ is determined by the connection of the voltage sources. B and C matrices are closely related.
D matrix $(m × m)$ is zero if only independent sources are considered.

Matrix x is  $(m + n) × 1$ and consist of unknown quantities, unknown nodal voltages and unknown current through the voltage sources.
Matrix z is  $(m + n) × 1$ and consist of the sum of the currents throught the passive elements and values of the independent voltage sources.
By following the rules for the creation of matrices we can create matrix Ax=z that can be calculated by using SciPy methods for calculation of sparse matrices.

### Limitations
Currently CircuitAnalyzer can work only with passive elements such as resistors and voltage sources. The work on current sources and other reactive elements is in the process.






