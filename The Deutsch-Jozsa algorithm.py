# Import necessary libraries
from qiskit import QuantumCircuit  # Import QuantumCircuit from Qiskit
import numpy as np  # Import NumPy for random number generation
from qiskit_aer import AerSimulator  # Import AerSimulator for running simulations



def dj_function(num_qubits):
    """
    Create a random Deutsch-Jozsa function.
    """
    
    # Initialize a quantum circuit with the specified number of qubits plus one ancilla qubit
    qc = QuantumCircuit(num_qubits + 1)
    
    # Randomly decide whether to flip the output qubit (ancilla) with a 50% chance
    if np.random.randint(0, 2):
        qc.x(num_qubits)  # Apply the X gate to the ancilla qubit to flip it to |1>
        
    # Randomly return a constant function with a 50% chance
    if np.random.randint(0, 2):
        return qc  # Return the circuit without further modifications

    # Choose half the possible input states for the balanced function
    on_states = np.random.choice(
        range(2**num_qubits),  # Sample from the range of numbers from 0 to 2^num_qubits
        2**num_qubits // 2,  # Specify the number of states to sample (half of all possible states)
        replace=False,  # Ensure that states are not repeated
    )

    def add_cx(qc, bit_string):
        """
        Add CX (CNOT) gates to the circuit based on a binary string.
        """
        # Loop through each bit in the reversed binary string
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":  # Apply the X gate to qubits corresponding to '1's in the string
                qc.x(qubit)
        return qc

    # Iterate through each selected state to create the function
    for state in on_states:
        qc.barrier()  # Add a barrier for visualization (optional)
        qc = add_cx(qc, f"{state:0b}")  # Add CNOT gates based on the current state
        qc.mcx(list(range(num_qubits)), num_qubits)  # Apply multi-controlled X gate
        qc = add_cx(qc, f"{state:0b}")  # Apply CNOT gates again to complete the function

    qc.barrier()  # Add another barrier for visualization

    return qc  # Return the constructed quantum circuit

# Generate a random Deutsch-Jozsa function and print the circuit
f = dj_function(3)
print(f.draw())  # Use print to show the circuit diagram




def compile_circuit(function: QuantumCircuit):
    """
    Compiles a circuit for use in the Deutsch-Jozsa algorithm.
    """
    n = function.num_qubits - 1  # Number of input qubits (excluding ancilla)
    qc = QuantumCircuit(n + 1, n)  # Create a new quantum circuit with n input qubits and one output qubit
    qc.x(n)  # Flip the output qubit to |1>
    qc.h(range(n + 1))  # Apply Hadamard gates to all qubits to create superposition
    qc.compose(function, inplace=True)  # Add the Deutsch-Jozsa function to the circuit
    qc.h(range(n))  # Apply Hadamard gates to input qubits again
    qc.measure(range(n), range(n))  # Measure the input qubits
    return qc  # Return the compiled circuit





def dj_algorithm(function: QuantumCircuit):
    """
    Determine if a Deutsch-Jozsa function is constant or balanced.
    """
    qc = compile_circuit(function)  # Compile the function circuit

    result = AerSimulator().run(qc, shots=1, memory=True).result()  # Run the simulation with one shot
    measurements = result.get_memory()  # Retrieve the measurement results
    if "1" in measurements[0]:  # Check if the measurement contains '1'
        return "balanced"  # Return "balanced" if '1' is found in the measurement
    return "constant"  # Otherwise, return "constant"

# Execute the Deutsch-Jozsa function and print the result
result_dj = dj_algorithm(f)
print(f"Dutch-Jozsa Result: {result_dj}")  # Print the result of the Deutsch-Jozsa algorithm




def bv_function(s):
    """
    Create a Bernstein-Vazirani function from a string of 1s and 0s.
    """
    qc = QuantumCircuit(len(s) + 1)  # Initialize a quantum circuit with the length of the string plus one
    for index, bit in enumerate(reversed(s)):  # Loop through the binary string in reverse
        if bit == "1":  # If the bit is '1', apply a CNOT gate
            qc.cx(index, len(s))  # Apply a CNOT gate from the input qubit to the ancilla qubit
    return qc  # Return the created quantum circuit

# Generate and print the Bernstein-Vazirani function circuit
bv_circuit = bv_function("1001")
print(bv_circuit.draw())  # Print the circuit diagram for the Bernstein-Vazirani function



