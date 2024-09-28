# Import the necessary modules from Qiskit and Matplotlib
from qiskit import QuantumCircuit  # Import the QuantumCircuit class to create quantum circuits
import matplotlib.pyplot as plt      # Import Matplotlib for plotting the circuit
from qiskit_aer import AerSimulator  # Import the AerSimulator for simulating quantum circuits




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




def compile_circuit(function: QuantumCircuit):
    """
    Compiles a circuit for use in Deutsch's algorithm.
    
    Parameters:
        function (QuantumCircuit): The quantum circuit representing the Deutsch function.
        
    Returns:
        QuantumCircuit: The compiled circuit ready for execution in Deutsch's algorithm.
    """
    # Determine the number of input qubits (excluding the output qubit)
    n = function.num_qubits - 1
    
    # Create a new QuantumCircuit with (n + 1) qubits and n classical bits for measurement
    qc = QuantumCircuit(n + 1, n)

    # Apply a Pauli-X gate to the last qubit (ancilla qubit) to prepare it in the |1⟩ state
    qc.x(n)
    
    # Apply Hadamard gates to all qubits to create superpositions
    qc.h(range(n + 1))

    # Add a barrier to separate stages in the circuit for better visualization
    qc.barrier()

    # Compose the provided function into the new circuit, modifying it in place
    qc.compose(function, inplace=True)
    
    # Add another barrier for clarity in the circuit visualization
    qc.barrier()

    # Apply Hadamard gates again to all input qubits (not the ancilla) to set up for measurement
    qc.h(range(n))
    
    # Measure the input qubits into the classical bits; results will be stored in the classical register
    qc.measure(range(n), range(n))

    # Return the compiled circuit, which is ready for execution
    return qc



# Create the Deutsch function circuit for case 3
deutsch_circuit = deutsch_function(3)

# Compile the circuit for Deutsch's algorithm
compiled_circuit = compile_circuit(deutsch_circuit)

# Draw and display the compiled circuit
fig = compiled_circuit.draw('mpl')  # Use Matplotlib drawer
plt.show()  # Show the drawn circuit





def deutsch_algorithm(function: QuantumCircuit):
    """
    Determine if a Deutsch function is constant or balanced.
    
    Parameters:
        function (QuantumCircuit): The quantum circuit representing the Deutsch function.
        
    Returns:
        str: "constant" if the function is constant, "balanced" if the function is balanced.
    """
    # Compile the input Deutsch function into a circuit suitable for execution
    qc = compile_circuit(function)

    # Create an AerSimulator instance to run the circuit simulation
    simulator = AerSimulator()

    # Run the compiled quantum circuit with a single shot and request memory output
    result = simulator.run(qc, shots=1, memory=True).result()
    
    # Retrieve the measurement results from the simulation
    measurements = result.get_memory()
    
    # Determine if the function is constant or balanced based on the measurement
    if measurements[0] == "0":
        return "constant"  # If the measurement is "0", the function is constant
    return "balanced"  # Otherwise, the function is balanced





def deutsch_algorithm(function: QuantumCircuit):
    """
    Determine if a Deutsch function is constant or balanced.
    
    Parameters:
        function (QuantumCircuit): The quantum circuit representing the Deutsch function.
        
    Returns:
        str: "constant" if the function is constant, "balanced" if the function is balanced.
    """
    # Compile the input Deutsch function into a circuit suitable for execution
    qc = compile_circuit(function)

    # Create an AerSimulator instance to run the circuit simulation
    simulator = AerSimulator()

    # Run the compiled quantum circuit with a single shot and request memory output
    result = simulator.run(qc, shots=1, memory=True).result()
    
    # Retrieve the measurement results from the simulation
    measurements = result.get_memory()
    
    # Determine if the function is constant or balanced based on the measurement
    if measurements[0] == "0":
        return "constant"  # If the measurement is "0", the function is constant
    return "balanced"  # Otherwise, the function is balanced


# Create the Deutsch function circuit for case 3
f = deutsch_function(3)

# Draw the circuit
fig = f.draw('mpl')  # Use Matplotlib drawer to draw the circuit
plt.show()  # Display the drawn circuit

# Run the Deutsch algorithm and display the result
result = deutsch_algorithm(f)
print(f"The Deutsch function is: {result}")  # Output the result
