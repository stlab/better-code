---
title: Concurrency
---

## Concurrency

%speaker
: Loosely, _concurrency_ is performing multiple tasks at once. A task is a conceptual unit of work, similar to a function but tasks don't have to be defined on function boundaries. The _granularity_ (or _grain size_) of a task is the amount of of work a task performs. The environment within which a task executes in the _execution context_. The hardware used to execute a task is the _execution agent_.
>
> Concurrency allows for increased _throughput_, the amount of work that can be completed in a given amount of time, by utilizing additional available agents. Concurrency also allows for lower _latency_, the amount of time between when a task is submitted and when it is completed. In this chapter, we will be dealing with concurrent computation, as opposed to concurrent IO, although the two ideas are closely related. <!-- Strike this if we have room to cover IO -->

<!--
Either here or later make the point that throughput and latency are in tension and must be balanced.
-->

- Loosely, performing multiple _tasks at once_
- Allows increased _throughput_ through better hardware utilization
- Allows decreased _latency_
- A _task_ is a _conceptual_ unit of (serial) work
  - May be composed of other tasks
  - Executes within an _execution context_
  - The hardware used to execute a task is the _execution agent_

- Concurrency is about having multiple task in flight at once

### Forms of Concurrency

%speaker
: _At once_ can mean any combination of _parallel_ or _interleaved_ execution. _Parallel_ execution is simultaneous execution using independent execution agents. _Interleaved_ execution is reallocating agents from one task to another. The procedure of reallocating agents from one task to another is a _context switch_.
>
> Interleaved execution may be scheduled in one of three different ways. _Preemption_ is interrupting one task, usually at a given time interval or when _waiting_, and switching to another task. _Cooperative_ is when a task explicitly _yields_ or _awaits_ at points when a context switch may occur. _Queued_ tasks run to completion and then another task is started. <!-- Say something about queued items may not be executed in the order they were enqueued? -->

- _At once_ can mean any combination of:
  - _Parallel_ (simultaneous) execution, with tasks using independent hardware
  - Interleaved
    - A _context switch_ is the procedure of reallocating hardware resources from one task to another
    - _Preemptive_: the system decides when to reallocate hardware to tasks
      - Provides illusion of parallelism
    - _Cooperative_: tasks _yield_ or _await_ when context switches may occur
    - _Queued_: tasks are run to completion and then another task is started

### Why Concurrency Matters

<!--
Come back to this section - prior is good but not happy with it.
-->

- Moore's law ends: Free Lunch is Over
  - Increasing difficult to push single core performance so more cores
  - To continue to improve throughput and latency requires concurrency
  - Latency is a key measure for interactivity

- I/O throughput and latency
  - Increased reliance on cloud technology

- Heterogeneous compute
  - Special-purpose agents (GPUs, Neural Engines, PGAs, specialized components)
  - Asymmetric cores

### Amdahl's Law

%speaker
: Amdahl's Law shows the challenge of unlocking performance through concurrency. Even with no overhead, having only 10% of a program serialize on a 16 processor machine will only see a 6.4x speedup compared to a single core. Amdahl's Law also shows the potential performance improvements of additional concurrency - eliminating that last 10% of serialized execution would unlock an additional 2.5x performance gain.

<!--
Two column with Amdahl's equation?
-->

<div style="text-align:center" markdown="1">
![](./img/amdahls-law.svg){:height="770"}
</div>

### Why Concurrency Is Hard

<!--
Might delete this section - would like to "discover" why it is hard
-->

- Reasoning about the visibility of effects is hard
- _then_ is a 4-letter word

### Forking and Joining Tasks

- Using _pure_ functions to represent tasks, consider the following:

```cpp
auto r = f(x) * g(x);
```

- `f()` and `g()` can be executed concurrently
  - _Forking_ is initiating a concurrent task
- Both `f()` and `g()` must complete before `operator*()` can be applied
  - _Joining_ is the process of receiving information, such as the result, of a concurrent task

### Spawning and Joining Tasks

- This might be represented as:

```cpp
auto g_ = fork([&]{ return g(x) }]); // execute concurrently
auto f_ = f(x);
auto r = f_ * join(g_);
```

- There are many different models for `fork()` and `join()`

### Threads

- Provide a unified view of concurrency and parallelism, preemptively scheduled
- Threads are the primary way to access parallelism from within a single program
  - OS processes provide concurrency and parallelism across programs

### Thread Example

```cpp
// Fork
decltype(g(x)) g_;
std::thread thread{[&]{
    g_ = g(x);
}};

auto f_ = f(x);

// Join
thread.join();

auto r = f_ * g_;
```

### Cost of Threads

%speaker
: The cost of thread context switches is a combination of kernel calls which require switching between protection rings, and cache invalidation
>
> Wired memory is not paged-out by the VM system. If memory is under pressure a thread, even if idle, imposes a performance penalty on the system <!-- Description of hyper-threading? -->

- Creation
  - Constructing and joining a thread ≈ 60,000 cycles
    - Additional cost of constructing and destructing all thread-local variables
  - Memory ≈ 0.5 MB for stack, memory is often _wired_
- Context switch
  - Direct cost ≈ 2,000 cycles
  - Total cost including cache invalidation ≈ 10,000 - 1,000,000 cycles

<!--
Reference: http://ithare.com/infographics-operation-costs-in-cpu-clock-cycles/
-->

### Thread Context Switches

- Context switches occur when there are more threads than execution agents (cores)
  - Context switches occur at intervals
  - Blocking the current thread (such as with `join()` will allow a context switch
- Ideal is one active thread per core

### Thread Pools

- A thread pool typically has one thread per core
  - The OS often provides a system thread pool (Apple and Microsoft)
- Tasks are queued to the pool
- Cost of queue is ≈ 100-500 cycles
- Since threads are joined at task completion, another mechanism is needed to communicate the result

### Communicating Between Concurrent Tasks and Races

%speaker
: A _race_ condition is when an order of effects is required for correct execution but that ordering is not guaranteed.
>
> Thread context switches are expensive because modern processors have dedicated memory caches per core. For the results of a core computation to be visible to another core requires a _memory fence_. A memory fence establishes an ordering of memory load and store operations. A memory fence must be understood by the processor and the compiler. If the compiler is not aware of a memory fence, it could reorder an operation so two threads would see inconsistent results.
>
> An evaluation that writes to a memory location while another evaluation reads or writes the same memory location is a _data race_ unless both are atomic operations or one of the conflicting operations _happens-before_ as established with a memory fence. The result of a _data race_ is undefined behavior.

<!--
Example from bad-cow. Can this be reduced?
-->

```cpp
template <typename T>
class bad_cow {
    struct object_t {
        explicit object_t(const T& x) : data_m(x) {}
        atomic<int> count_m{1};
        T           data_m; };
    object_t* object_m;
 public:
    explicit bad_cow(const T& x) : object_m(new object_t(x)) { }
    ~bad_cow() { if (0 == --object_m->count_m) delete object_m; }
    bad_cow(const bad_cow& x) : object_m(x.object_m) { ++object_m->count_m; }

    bad_cow& operator=(const T& x) {
        if (object_m->count_m == 1) object_m->data_m = x;
        else {
            object_t* tmp = new object_t(x);
            --object_m->count_m;
            object_m = tmp;
        }
        return *this;
    }
};
```

### Waiting, Locking, and Deadlocks

```cpp
std::atomic_flag done;
decltype(g(x)) g_;

// fork
system_thread_pool([&]{
    g_ = g(x);
    done.test_and_set();
    done.notify_one();
}]);

auto f_ = f(x);

done.wait(false); // join (deadlock?)
auto r = f_ * g_;
```

### Continuations and Futures

```cpp
    // fork
    std::future<decltype(g(x))> g_ = async(system_thread_pool, [&]{ return g(x); });

    auto f_ = f(x);

    // join (deadlock?)
    return f_ * g_.get();
```

<!--
    Worth implementing this with callbacks to show the progression to futures?
-->

```cpp
    return stlab::when_all(stlab::async(system_scheduler, [=]{ return g(x); }),
                           stlab::async(system_scheduler, [=]{ return f(x); }) |
            [](const auto& a, const auto& b){ return a * b; });
```

```cpp
    return stlab::when_all(stlab::async(system_scheduler, [=]{ return g(x); }),
                           stlab::async(system_scheduler, [=]{ return f(x); }) |
            [](const auto& a, const auto& b){ return a * b; });
```

<!--
    We need a discussion of grain size.
-->

### Cancellation

### Sender/Receiver Model

### Serial Queues and Actors

### Channels

### Coroutines and Fibers

### The Exit Problem

### Closing thoughts

- If we look at our original problem statement

```cpp
    return f(x) * g(x);
```

- If we know that `f()` and `g()` do not share mutable state that is enough to execute these concurrently
  - Profile guided optimization could determine efficient grain sizes
