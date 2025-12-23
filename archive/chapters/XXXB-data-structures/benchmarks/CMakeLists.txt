cmake_minimum_required(VERSION 3.20)
project(stlab_benchmarks)
# enable_testing()

include(FetchContent)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_CXX_EXTENSIONS NO)
set(CMAKE_BUILD_TYPE Release)

# Suppress google/benchmark internal tests
set(BENCHMARK_ENABLE_TESTING off)

FetchContent_Declare(googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG main)

FetchContent_Declare(googlebenchmark
        GIT_REPOSITORY https://github.com/google/benchmark.git
        GIT_TAG main) 

FetchContent_MakeAvailable(
        googletest
        googlebenchmark)

add_executable(stlab_benchmarks main.cpp)
target_link_libraries(stlab_benchmarks benchmark::benchmark)