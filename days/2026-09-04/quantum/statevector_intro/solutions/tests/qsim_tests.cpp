#include "qsim.hpp"
#include <cassert>
#include <cmath>
#include <iostream>

static bool near(double a, double b) {
    return std::fabs(a - b) < 1.0e-10;
}

int main() {
    {
        StateVector q(1);
        q.apply_x(0);
        assert(near(q.probability(0), 0.0));
        assert(near(q.probability(1), 1.0));
        assert(near(q.norm_squared(), 1.0));
    }

    {
        StateVector q(1);
        q.apply_h(0);
        assert(near(q.probability(0), 0.5));
        assert(near(q.probability(1), 0.5));
        assert(near(q.norm_squared(), 1.0));
    }

    {
        StateVector bell(2);
        bell.apply_h(0);
        bell.apply_cnot(0, 1);
        assert(near(bell.probability(0), 0.5));
        assert(near(bell.probability(3), 0.5));
        assert(near(bell.probability(1), 0.0));
        assert(near(bell.probability(2), 0.0));
        assert(near(bell.norm_squared(), 1.0));
    }

    std::cout << "chris-qsim tests passed\n";
}
