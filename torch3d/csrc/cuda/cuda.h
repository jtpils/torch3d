// -*- mode: c++ -*-
#include <torch/extension.h>
#include <ATen/cuda/CUDAContext.h>


at::Tensor farthest_point_sample_cuda(const at::Tensor& points, int num_samples);
at::Tensor ball_point_cuda(const at::Tensor& points, const at::Tensor& queries, float radius, int k);
at::Tensor gather_points_cuda(const at::Tensor& points, const at::Tensor& indices);
at::Tensor gather_points_backward_cuda(const at::Tensor& grad, const at::Tensor& indices, int n);
std::pair<at::Tensor, at::Tensor> three_nn_cuda(const at::Tensor& points, const at::Tensor& queries);
