# Architecture

A deterministic queue transports messages across an undirected topology. Each peer tracks message IDs it has already seen, preventing loops from creating infinite propagation. TTL provides an explicit propagation bound.
