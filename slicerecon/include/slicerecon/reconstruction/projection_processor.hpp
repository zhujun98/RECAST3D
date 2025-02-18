#pragma once

#include <cmath>
#include <complex>
#include <vector>

extern "C" {
#include <fftw3.h>
}

#include <bulk/backends/thread/thread.hpp>
#include <bulk/bulk.hpp>

#include "../data_types.hpp"

namespace slicerecon {

namespace filter {

std::vector<float> ram_lak(int cols);
std::vector<float> shepp_logan(int cols);
std::vector<float> gaussian(int cols, float sigma);
std::vector<float> paganin(int rows, int cols, float pixel_size, float lambda,
                           float delta, float beta, float distance);
} // namespace filter

namespace detail {

struct Projection {
    float* data;
    int rows;
    int cols;
};

struct Flatfielder {
    Projection dark;
    Projection reciproc;

    void apply(Projection proj) const;
};

struct Neglogger {
    void apply(Projection proj) const;
};

struct FDKScaler {
    std::vector<float> weights;
    void apply(Projection proj, int proj_idx) const;
};

struct Paganin {
    Paganin(Settings param, Geometry geom, float* data);

    void apply(Projection proj, int s);

  private:
    fftwf_plan fft2d_plan_;
    fftwf_plan ffti2d_plan_;
    std::vector<std::vector<std::complex<float>>> proj_freq_buffer_;
    std::vector<float> paganin_filter_;
    PaganinSettings paganin_;
};

class Filterer {
  public:
    Filterer(Settings param, Geometry geom, float* data);

    void set_filter(std::vector<float> filter);

    void apply(Projection proj, int s, int proj_idx);

  private:
    std::vector<std::vector<std::complex<float>>> freq_buffer_;
    std::vector<float> filter_;
    fftwf_plan fft_plan_;
    fftwf_plan ffti_plan_;
};

} // namespace detail

class ProjectionProcessor {
  public:
    ProjectionProcessor(Settings param, Geometry geom);

    void process(float* data, int proj_id_begin, int proj_id_end);

    std::unique_ptr<detail::Flatfielder> flatfielder;
    std::unique_ptr<detail::Neglogger> neglog;
    std::unique_ptr<detail::Filterer> filterer;
    std::unique_ptr<detail::Paganin> paganin;
    std::unique_ptr<detail::FDKScaler> fdk_scale;

  private:
    Settings param_;
    Geometry geom_;

    bulk::thread::environment env_;
};

} // namespace slicerecon
