#include <tuple>
#include <vector>
#include <utility>

#include <benchmark/benchmark.h>

// Notably, almost the same performance for SIZE ~= 10'000'000;
// After 1b, we start to see about an order-of-magnitude difference.
constexpr auto SIZE = 1'000'000'000;

struct Object {
    int x, y, z, a, b, c;
};

template <class T>
struct Pairwise {
    std::vector<std::pair<T, bool>> pairs;

    Pairwise(std::size_t init_size) : pairs(init_size) {}

    decltype(auto) operator[](std::size_t idx) {
        return pairs[idx];
    }
};

template <class T>
struct Separate {
    std::vector<T> ts;
    std::vector<bool> bools;

    Separate(std::size_t init_size) : ts(init_size), bools(init_size) {}

    decltype(auto) operator[](std::size_t idx) {
        return std::forward_as_tuple(ts[idx], bools[idx]);
    }
};

static void BM_Pairwise(benchmark::State& state) {
    // Perform setup here
    Pairwise<Object> p(SIZE);   

    for (auto _ : state) {
        for (auto i(0); i < SIZE; ++i) {
            benchmark::DoNotOptimize(p[i] = 
                std::make_tuple(Object{i, i, i, i, i, i}, i % 2 == 0));
        }
    }
}

static void BM_Separate(benchmark::State& state) {
    // Perform setup here
    Separate<Object> s(SIZE);   

    for (auto _ : state) {
        for (auto i(0); i < SIZE; ++i) {
            benchmark::DoNotOptimize(s[i] = 
                std::make_tuple(Object{i, i, i, i, i, i}, i % 2 == 0));
        }
    }
}

BENCHMARK(BM_Pairwise);
BENCHMARK(BM_Separate);

// Run the benchmark
BENCHMARK_MAIN();