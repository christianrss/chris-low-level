# Chris QSim

## Problem
Quantum frameworks can obscure the simplest classical representation of a quantum state: a vector of 2^n complex amplitudes.

## Current milestone
A CPU state-vector simulator with X, H, Z and CNOT gates, norm/probability inspection and Bell-state tests.

## Research angle
The benchmark records exponential state growth explicitly. Later milestones compare memory layout, SIMD, threading, GPU kernels, stabilizer simulation and tensor networks.

## Limitations
This is a noiseless educational simulator with no measurement sampler, circuit IR or hardware backend yet. It makes no claim of quantum advantage.
