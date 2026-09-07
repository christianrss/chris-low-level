#pragma once
#include <vector>
#include "depth_buffer.hpp"

bool parity_scene_cpu(std::vector<depth_lab::Color>& fb, depth_lab::DepthBuffer& db);
