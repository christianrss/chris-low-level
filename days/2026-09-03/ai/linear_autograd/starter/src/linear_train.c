#include <stdio.h>

int main(void) {
    const double xs[] = {1.0, 2.0, 3.0, 4.0};
    const double ys[] = {3.0, 5.0, 7.0, 9.0};
    const int count = 4;

    double weight = 0.0;
    double bias = 0.0;
    const double learning_rate = 0.01;

    for (int epoch = 0; epoch < 1000; ++epoch) {
        double d_weight = 0.0;
        double d_bias = 0.0;

        for (int i = 0; i < count; ++i) {
            const double prediction = weight * xs[i] + bias;
            const double error = prediction - ys[i];

            // TODO: derive and accumulate dL/dw and dL/db.
            (void)error;
        }

        // TODO: average the gradients over the batch.
        // TODO: perform the SGD update.
        (void)d_weight;
        (void)d_bias;
        (void)learning_rate;
    }

    printf("w=%.6f b=%.6f\n", weight, bias);
    return 0;
}
