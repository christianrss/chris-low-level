# Architecture

Three cursors model producer, device and consumer progress. Ownership changes are explicit. This approximates the bookkeeping pattern used by real hardware queues without pretending to emulate a particular NIC.
