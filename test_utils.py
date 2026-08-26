import unittest

import cirq

from utils import build_routed_circuit


class BuildRoutedCircuitTests(unittest.TestCase):
    def test_build_routed_circuit_includes_terminal_measurement(self) -> None:
        qubit_map = {index: (index // 4, index % 4) for index in range(11)}

        circuit = build_routed_circuit(qubit_map=qubit_map, CX_gates=[])

        measurement_operations = [
            operation
            for operation in circuit.all_operations()
            if isinstance(operation.gate, cirq.MeasurementGate)
        ]
        self.assertEqual(len(measurement_operations), 1)
        self.assertEqual(len(measurement_operations[0].qubits), 10)


if __name__ == "__main__":
    unittest.main()

