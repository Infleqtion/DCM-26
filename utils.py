import cirq
import numpy as np

SHAPE = (4, 4)
qubits = np.reshape(np.array(cirq.GridQubit.square(4)), SHAPE)

def build_routed_circuit(
    qubit_map: dict[int, tuple[int, int]], CX_gates: list[tuple[tuple[int, int], tuple[int, int]]]
) -> cirq.Circuit:
    ops = [
        cirq.X(qubits[qubit_map[10]]),
        cirq.H.on_each([qubits[v] for _, v in qubit_map.items()])
    ]
    for ctrl, trgt in CX_gates:
        if not verify_gate(ctrl, trgt):
            raise ValueError(f"The CX gate controlled by {ctrl} and targeting {trgt} does not match the grid topology.")
        ops.append(cirq.CX(qubits[ctrl], qubits[trgt]))
    ops += [cirq.H.on_each([qubits[qubit_map[k]] for k in range(10)])]
    cirq.measure(*[qubits[qubit_map[k]] for k in range(10)])
    return cirq.Circuit(ops)


def verify_gate(ctrl: tuple[int, int], trgt: tuple[int, int]) -> bool:
    if not (
        (0 <= ctrl[0] < SHAPE[0]) and 
        (0 <= ctrl[1] < SHAPE[1]) and 
        (0 <= trgt[0] < SHAPE[0]) and
        (0 <= trgt[1] < SHAPE[1])
    ):
        return False
    if not (
        ((ctrl[0] == trgt[0]) and abs(ctrl[1] - trgt[1]) == 1) or 
        ((ctrl[1] == trgt[1]) and abs(ctrl[0] - trgt[0]) == 1)
    ):
        return False
    return True
    