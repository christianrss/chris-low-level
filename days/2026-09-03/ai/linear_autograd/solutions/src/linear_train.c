#include <math.h>
#include <stdio.h>

static double predict(double x, double weight, double bias) {
    return weight * x + bias;
}

static double mean_squared_error(
    const double *xs,
    const double *ys,
    size_t count,
    double weight,
    double bias) {

    double total = 0.0;

    for (size_t i = 0; i < count; ++i) {
        const double error = predict(xs[i], weight, bias) - ys[i];
        total += error * error;
    }

    return total / (double)count;
}

int main(void) {
    const double xs[] = {1.0, 2.0, 3.0, 4.0};
    const double ys[] = {3.0, 5.0, 7.0, 9.0};
    const size_t count = sizeof(xs) / sizeof(xs[0]);

    double weight = 0.0;
    double bias = 0.0;
    const double learning_rate = 0.01;

    for (int epoch = 0; epoch < 1000; ++epoch) {
        double d_weight = 0.0;
        double d_bias = 0.0;

        for (size_t i = 0; i < count; ++i) {
            const double prediction = predict(xs[i], weight, bias);
            const double error = prediction - ys[i];

            // These are the analytical derivatives of (prediction - y)^2.
            d_weight += 2.0 * error * xs[i];
            d_bias += 2.0 * error;
        }

        // We optimize the mean loss, so the batch gradients are averaged too.
        d_weight /= (double)count;
        d_bias /= (double)count;

        weight -= learning_rate * d_weight;
        bias -= learning_rate * d_bias;
    }

    const double loss = mean_squared_error(xs, ys, count, weight, bias);
    printf("w=%.6f b=%.6f mse=%.9f\n", weight, bias, loss);

    if (fabs(weight - 2.0) > 0.02 || fabs(bias - 1.0) > 0.05) {
        fprintf(stderr, "training did not converge to the expected line\n");
        return 1;
    }

    return 0;
}
