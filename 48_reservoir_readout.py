"""48_reservoir_readout.py — A tiny reservoir + perceptron on synthetic data.

Demonstrates: the reservoir idea at teaching size — a fixed
random projection expands the input, and only a simple
perceptron readout is trained. Data here is synthetic (two
clearly separated pattern families), so the lesson is the
architecture, not any claim about real signals.
Run: python3 48_reservoir_readout.py
"""

import random


def make_patterns(rng, count):
    """Two synthetic families: high-first-half vs high-second-half."""
    data = []
    for i in range(count):
        label = i % 2
        if label == 0:
            pattern = [rng.uniform(0.7, 1.0) if j < 8 else rng.uniform(0.0, 0.3)
                       for j in range(16)]
        else:
            pattern = [rng.uniform(0.0, 0.3) if j < 8 else rng.uniform(0.7, 1.0)
                       for j in range(16)]
        data.append((pattern, label))
    return data


def project(pattern, weights):
    """Fixed random projection: 16 inputs -> 24 reservoir features."""
    return [max(0.0, sum(w * x for w, x in zip(row, pattern)))
            for row in weights]


def train_perceptron(features, labels, epochs=30, rate=0.1):
    weights = [0.0] * len(features[0])
    bias = 0.0
    for _ in range(epochs):
        for feats, label in zip(features, labels):
            score = sum(w * x for w, x in zip(weights, feats)) + bias
            pred = 1 if score >= 0 else 0
            error = label - pred
            weights = [w + rate * error * x for w, x in zip(weights, feats)]
            bias += rate * error
    return weights, bias


def accuracy(weights, bias, features, labels):
    correct = 0
    for feats, label in zip(features, labels):
        pred = 1 if sum(w * x for w, x in zip(weights, feats)) + bias >= 0 else 0
        correct += int(pred == label)
    return correct / len(labels)


def main():
    rng = random.Random(7)
    reservoir = [[rng.uniform(-1, 1) for _ in range(16)] for _ in range(24)]
    train = make_patterns(rng, 100)
    test = make_patterns(rng, 40)
    train_feats = [project(p, reservoir) for p, _ in train]
    test_feats = [project(p, reservoir) for p, _ in test]
    weights, bias = train_perceptron(train_feats, [y for _, y in train])
    acc = accuracy(weights, bias, test_feats, [y for _, y in test])
    assert acc >= 0.9  # synthetic families are well separated
    print(f"PROOF: reservoir readout accuracy on 40 held-out synthetic "
          f"patterns = {acc:.1%} (chance = 50%)")


if __name__ == "__main__":
    main()
