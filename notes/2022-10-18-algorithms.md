# 2022-10-18
** Attendees **: Sean Parent, Nick DeMarco

# Notes

How do you construct code, given a contract.
The process should be iterative
Start with an idea, usually around the postconditions.
What do you want this function to _do_ / what's the result?
In doing so, you discover what's required of it. 
You "back into" the preconditions.

Starting with postc is "top down", we figure out what's required to meet those postconditions

Steer clear of formal proofs, but can we reason about our functions and be confident the postcs hold.

The name of a function comes from naming the postconditions
    If two functions have identical postcs, do they always have the same name?
        sometimes, you might specialize the name of a function given context, arguments, etc.
        might have different vocabulary in different domains (where domain is arguments to function)
            graphic might use one term, mathematics another
        once you get down to a concrete case, sometimes helpful to augment the name
        tendency: people discover you can probably implement all of STL into map reduce (certainly scan + map reduce)
            Conor Hoekstra: https://www.youtube.com/watch?v=w37XnvIf6qE
            composing algorithms out of other algorithms (everything is a scan or a reduction)
            problem: scan & reduction have almost no postconditions
                reduction doesn't tell you what the thing "does"; it's an implementation pattern.
                gets into category theory: patterns for how things compose
                    devoid of semantics; not useless, though.
                    scan, scan, scan, reduce, reduce, reduce, are basically raw loops.
                        scan is another way to spell "for", it's not adding semantics.
                        reduce is a complicated for loop
                    It's a little better than just a loop, but not much better.

The postcs define the semantics of the op
Language: associate a name with a set of semantics, building up a vocabulary
stdlib is not just a library, it's a vocabulary. If you're finding something, probably want to call it `find`, maybe with qualifications.

Complexity of an operation is part of the semantics of the operation
    This gets left out in a lot of CS
    Noun as constant time op, verb as linear time op
    see: forest library in ASL
        (linked structure with no backlinks). 
        algoritm to get parent of an iterator was named `parent`, but was linear time.
        to find parent, run to end of siblings until you get back up the tree.
        but of course, someone wrote "for each of my children, find its parent" O(N^2)
    
    What about logn time? nlogn time? What about quadradic functions? How do we name these things?
        In all practicality, logn and poly-logn is treated as constant. (some polynomial in logn)
        Therefore, nlogn and poly-nlogn is treated as linear
        After that, you quickly approach algorithms that don't terminate
            There are n^2 that are more efficient, NP complete you want to solve
                but when you're in those domains, you're working on a supercomputer, grinding away (or quantum)
                Or you're talking about efficiency with small data sets (due to cache locality)
    For n^2 and more complex, advice is to put complexity in the name "nSquaredSort"; precondition that N is small or this doesn't terminate. 

    People tend to overthink big-O notation, and ignore physicality of machine (cache locality, ordering, ignore K)

    Super optimized function might take linear time to Klogn, but if K is very high, most uses of the algorithm will be a pessimization.

    Talk less about Big-O, talk about operation counts. In generic code, that's especially important. Complexity of your algorithm is dependent on the complexity of the subroutine provided. "Apply the compare operation logN times".
        You can do a binsearch on a linked list, but that's going to be linear time (n + logn, not logn)
        Binsearch on linked list will traverse twice, rather than a linear search that traverses once. You search twice as many items
        Is a binsearch efficient or not? Depends on the ratio of getting the next element and doing the compare function.
            find: n/2 increments, n/2 compares
            binsearch: n increments, and logn compares.

        It can be more useful to ignore big-O notation and talk about operation counts.

Building up the function, and reasoning about it:
    loops; start with `find`.
        when we hit the loop, what do we have to reason about?
            will it terminate? 
                expressed as "something is getting smaller with each iteration"
                what is reducing?
                the desired postcondition of the loop has to hold
            Need to be able to reason at each step of the loop, we're getting closer to the postc.
                "some property holds until termination"
            
            will kick up dafny to express this (but dafny will not appear in the book, except as an appendix, possibly online)

        start with find in some other context - we want to "discover find" out of some larger program specification.

        Once we state the postcs of the loop, we've defined the semantics of the loop
            reasoning about the loop has a pretty high bar, so we should encapsulate and name it. 
            this is the "no raw loops" conclusion

    Binary search, to "drive the point home"
        start with homework on binsearch - ala photoshop enterance exam (description of lower bound)
        build out the correct answer, discuss common pitfalls. 
        we need something reducing at each loop step, half open ranges make that much simpler
            when you see "while (i < n)", it seems the author doesn't know exactly when the loop will terminate.
            `i < n` as code smell; 
            is `i` changing? is `n` changing? why the uncertainty?
                people argue it's safer: is it safer? I'd rather a coding error hang my app

    two main ways to reason about an algorithm
        1. iteratively (some property holds at point x, how to make it work at x + 1)
        2. divide and conquer (some property holds for two halves of my data, how can I combine those two?)
    
    problems solvable in a linear sense can be solved faster (but less efficiently) in parallel with a divide and conquer approach
        linear find can be done in parallel, but this is similar to binsearch on a linked list
            take my vector of things, give halves to one cpu each
            on average, one cpu will have to search the whole space, the other will (on average) search half of the space.
            so I'm searching 75% of my vector on average, instead of 50% of the space on average.
                a motivation for efficient cancellation; you can tell the half doomed to search its whole space to stop looking when its found. this motivates non-blocking cancellation
        
        google was born out of the realization that every problem can be expressed as a map-reduce problem
            map-reduce is trivially parallelizable. if I can add a million CPUs, I can solve a huge class of problems nearly instantly. 

    note: for a given algorithm, there's an in-situ implementation, and a functional implementation
        functional can either be greedy or lazy
        Slide & Gather
            when you're trying to solve a problem, you can figure out how to divide the problem into simpler algorithms
            slide is rotate; gather is 2 stable partitions.
            most algorithms are not written in terms of loops, they're written in terms of other algorithms
            stable_partition is nice, because in-situ stable_partition can be composed out of rotates. (see C++ seasoning / a9 extended version of seasoning)

        decomposing s_p can be done in-situ with rotate,
            but easier to do functionally (you can make copies, do in linear time with extra memory)
                STL version defined to be memory-adaptive. 
                    if you have the memory, you can do it functionally, until you start paging the VM (then switch to in-situ)
                    rotate version is divide & conquer, cutting the range in half
                        need to ask, "how much memory do I have before I hit the VM system?"
                            then subdivide to that size, and do a linear one
                    the problem is: alex's original version of STL has a function called "get_temp_buffer"
                        implemented as `malloc` with a comment as to what it should do (but all modern implementations just do malloc)
                these days, probably never matters
                    very rarely doing a stable_partition on things that don't fit into physical memory

            s_p can be done lazily
                not as horrible as you might think; 
                an interesting exercise: implement a lazy stable partition, and implement gather in terms of it
                goal: show students it's completely doable, complexity is not as bad as you'd think at first
                out of it, you get a functional gather operation
                non-trivial problem
                fear: too much functional composition that make inefficient code look efficient w/ range composition
                most devs without a haskell background (in industry) have little awareness and intuition of lazy algorithms
                goal: have them work through a meaningful lazy algorithm. 

                in-situ stable partition can be done as partition the halves, and do a rotate.
                can implement stable_partition in terms of recursive lazy stable_partition
                intuition: divide and conquer will be horrible, morass of lazy objects (no, because you only work on one section of the tree at a time)

                how would you do a lazy gather? need a lazy stable_partition1

        how often do we discard algorithms composed as other algorithms, in favor of fine-tuned performance for special cases?
            lazy evaluation, in particular, is very good at composing scan algorithms efficiently. composed into a single pass.
                vs a greedy scan which will turn into multiple passes.
            there aren't that many interesting scan algorithms
                this gets more attention than it should. 
                niebler constructs a calendar out of composed scan algorithms (to the delight of the functional community)
                the lazy evaluation composition doesn't give you single pass, it ends up being less efficient
                    yet the code looks identical to an efficient implementation
                rare to find places where it's efficient to compose well
                for scan algorithms in particular, build up a rich set of scan algorithms
                    lots of variants of `find`, `copy`, etc.
                        finds that terminate quickly, copies that terminate under some condition (copy_until, copy_if, etc)
                        with a rich set of these, that handles 99% of the beautiful functional-scan compositions.
            
            typically, fusing two operations for a performance win is more general than you think
                whether it's lazily composed (copy_until == copy + find), or hand-rolled.
                    what are the semantics of the fused operation? lift it, give it a name. there aren't that many interesting cases that fuse like that.
            
                