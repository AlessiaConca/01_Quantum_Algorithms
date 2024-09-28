# Import the necessary modules from Qiskit and Matplotlib
from qiskit import QuantumCircuit  # Import the QuantumCircuit class to create quantum circuits
import matplotlib.pyplot as plt      # Import Matplotlib for plotting the circuit

def deutsch_function(case: int):
    """
    Generate a valid Deutsch function as a `QuantumCircuit`.
    
    Parameters:
        case (int): An integer representing the specific Deutsch function to generate.
                     Must be one of the values: 1, 2, 3, or 4.
    
    Returns:
        QuantumCircuit: A quantum circuit representing the selected Deutsch function.
    """
    # Raise an error if the case is not within the valid range
    if case not in [1, 2, 3, 4]:
        raise ValueError("`case` must be 1, 2, 3, or 4.")

    # Initialize a QuantumCircuit with 2 qubits
    f = QuantumCircuit(2)
    
    # Apply a controlled NOT (CNOT) gate if case 2 or 3 is selected
    if case in [2, 3]:
        f.cx(0, 1)  # CNOT gate: flips the second qubit if the first qubit is |1>
    
    # Apply a Pauli-X gate (NOT gate) on the second qubit if case 3 or 4 is selected
    if case in [3, 4]:
        f.x(1)  # Pauli-X gate: flips the state of the second qubit

    # Return the generated quantum circuit
    return f

# Create the circuit by calling the deutsch_function with case 3
qc = deutsch_function(3)

# Draw the circuit using Matplotlib and display it
fig = qc.draw('mpl')  # Draw the quantum circuit in a format suitable for Matplotlib
plt.show()            # Display the drawn circuit
