"""50_signal_bands.py — Band power from a synthetic signal (teaching size).

Demonstrates: the idea behind frequency-band analysis — take
a short synthetic signal, compute a small discrete Fourier
transform in pure Python, and sum power in a low band and a
high band. A slow wave lands in the low band; a fast wave
lands in the high band. Data is synthetic; no claim about
any real recording is made here.
Run: python3 50_signal_bands.py
"""

import cmath
import math


def dft_magnitudes(samples):
    """Naive DFT magnitudes; fine for short teaching signals."""
    n = len(samples)
    out = []
    for k in range(n):
        total = sum(samples[t] * cmath.exp(-2j * math.pi * k * t / n)
                    for t in range(n))
        out.append(abs(total))
    return out


def band_power(magnitudes, sample_rate, low_hz, high_hz):
    n = len(magnitudes)
    power = 0.0
    for k, mag in enumerate(magnitudes):
        freq = k * sample_rate / n
        if low_hz <= freq < high_hz:
            power += mag ** 2
    return power


def main():
    rate, n = 64, 64  # 1 second of samples at 64 Hz
    slow = [math.sin(2 * math.pi * 4 * t / rate) for t in range(n)]
    fast = [math.sin(2 * math.pi * 24 * t / rate) for t in range(n)]
    slow_mags = dft_magnitudes(slow)
    fast_mags = dft_magnitudes(fast)
    # Low band 2-8 Hz, high band 16-32 Hz.
    assert band_power(slow_mags, rate, 2, 8) > band_power(slow_mags, rate, 16, 32)
    assert band_power(fast_mags, rate, 16, 32) > band_power(fast_mags, rate, 2, 8)
    print("PROOF: 4 Hz synthetic wave -> power concentrated in the 2-8 Hz band")
    print("PROOF: 24 Hz synthetic wave -> power concentrated in the 16-32 Hz band")


if __name__ == "__main__":
    main()
