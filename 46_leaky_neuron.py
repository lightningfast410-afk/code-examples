"""46_leaky_neuron.py — A leaky integrate-and-fire neuron, teaching size.

Demonstrates: the simplest spiking-neuron model — membrane
voltage rises with incoming current, leaks toward rest, and
fires (then resets) when it crosses a threshold. Feed it a
steady current and it spikes regularly; feed it nothing and
it stays silent. A teaching model, not a brain simulation.
Run: python3 46_leaky_neuron.py
"""

REST = 0.0
THRESHOLD = 1.0
LEAK = 0.1
STEP = 0.1


def simulate(currents):
    """Return the list of time steps where the neuron spiked."""
    voltage = REST
    spikes = []
    for step, current in enumerate(currents):
        voltage += STEP * (-LEAK * (voltage - REST) + current)
        if voltage >= THRESHOLD:
            spikes.append(step)
            voltage = REST
    return spikes


def main():
    silent = simulate([0.0] * 50)
    assert silent == []
    # Steady strong current: regular spikes.
    steady = simulate([2.0] * 100)
    assert len(steady) >= 5
    gaps = [b - a for a, b in zip(steady, steady[1:])]
    assert max(gaps) - min(gaps) <= 1  # roughly periodic
    # A single brief pulse below threshold: no spike.
    pulse = simulate([0.0] * 10 + [5.0] + [0.0] * 20)
    assert pulse == []
    print(f"PROOF: no input -> {len(silent)} spikes")
    print(f"PROOF: steady input -> {len(steady)} spikes, gaps {sorted(set(gaps))}")
    print(f"PROOF: one brief pulse -> {len(pulse)} spikes (leak wins)")


if __name__ == "__main__":
    main()
