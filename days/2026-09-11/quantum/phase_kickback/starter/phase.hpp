#pragma once
void q_reset(double amp[4]);
void q_h0(double amp[4]);
void q_cz(double amp[4]); /* control q0 target q1: flip sign of |11> */
double q_prob(const double amp[4], int basis);
