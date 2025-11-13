# 2022-10-12
**Attendees**: Sean Parent, Nick DeMarco

Outline comes from the talks, primarily

Want Relationships to be a central theme

Each chapter starts with a pithy "don't do this" kind of phrase
- Then dig into what the actual problem is on a foundational level
- Give the necessary definitions, structure, build up the understanding. 
- "point to" solutions; don't give concrete prescriptions; give a few tools and modes of thinking; lead to an approach.
- help to teach you to think
- what are the essential relationships between these problems; how do we manage those relationships, to reason about these components locally. 
- The relationships chapter itself is a thorough description of what relationships actually are
- what is a value - the value is bits/atoms imbued with meaning; this is like language where we embue the sound "blue" with the platonic idea of blueness. 
    - How does the word "language" fit into this mental model?
    - The way we ascribe meaning to a function is to describe its postconditions.
    - It would be difficult to reason about your code if you just had lists of postconditions named "f, g, h", etc.
    - So what do we do? We give those postconditions, that meaning, a name. 
    - The English description of `min` "this returns the minimum of A and B". We have an English word for this. 
    - If you write the equation for what "minimum" means in code, it's challenging in the case that A and B are the same. 
    - It's the lesser of A and B, unless they're the same, in which case it's implementation-defined. It's the value. Conventionally A. 
    - The word, "min", naturally carries more meaning than the equation. The additional information is the encoding of what you do when they're the same. Whenever I use this name, I mean this set of postconditions. 
    - I can reduce my cognitive load by encapsulating postconditions inside the name.
    - When defining new vocabulary, you need an English definition of it. 
- relationship can have three states: it holds, it doesn't hold (which is severed, which is testable, or invalid, which means you can't even ask the question; AKA you can't write a predicate to test the state).
- There's no way to write a predicate without global knowledge of the system, and its history. (reminds me of classical theory of physics before quantum)
- an object that isn't a pointer also has the three states (it can hold, be severed, or invalid)
- `optional` lets us express severable relationships. 
- safety is about ensuring that nothing is ever invalid. avoid the "I can't even ask the question" state. We want to create systems where that's inforced and can't be violated.
- The problem is the relationship is in our minds, it's not in the code. 
    - If I have a turing complete system, super-safe, invalid is inexpressible. If it's turing complete, I can write a C machine, and then write more bad code. 
    - In reality, if you give a user a set of safe tools, but a user thinks about the problem in terms of shared_ptr, they will simulate how they're thinking about the problem within the super-safe system. 
    - So, you can't solve this problem from a technology standpoint. 
    - Ken Iverson: the notation can guide you, but it can't perfectly forbid invalid states.
- Better Code acknowledges that there is no silver technical bullet; there is no "royal road". 
- Reading this book won't make you a super programmer that doesn't write bad code. 
- It's very hard to think through relationships and encode them without contradictions.

- Relationships are a known entity that don't get discussed enough. It gets a little bit scattered. 
- Are relationships morphisms? 
    - We can classify relationships - what are the rules of implication?
    - How do relationships compose?
    - You end up building up a very rich calculus - comparable to category theory, abstract algebra, etc.
    - Category theory looks a lot at composition rules
    - abstract algebra looks more at calculation approach; an algorithmic approach ("what can you do/solve")
    - There's no way to write axioms to determine the properties of an input such that Euclid's algorithm terminates. 
        - Alex Stepanov worked on this for a long time and failed; 
        - On computers, we don't use Euclid's algorithm, we use [Josef Stein's](https://en.wikipedia.org/wiki/Binary_GCD_algorithm). 
        - Number systems can either be in the Euclidean domain, or the Stein Domain, but no proofs it _isn't_ in the other. 
            - Conjecture: they're the same, but it's an open problem.
- We borrow terminology a lot from database theory, which itself borrows from mathematics
    - One to many, many-to-many, etc.
- A constraint is a relationship
- Given a value A, map it to a value B, such that A -> B satisfies the relationship f()
    - Some functions are invertible, given a B, give me the A s.t. f(A) == B.
    - For some domains, the inverse is a set of values, possibly infinite. 

- Looking at code: what relationships do I have at my disposal?
- Contracts are a set of postconditions/preconditions (both are relationships)
    - These have to hold; for an operation, what am I given? what are the essential relationships between objects in this space? We need to ignore irrelevant relationships. 
    - What are the mappings I can do to get from A to B? How can I exploit things?
- Russian Coat Check Algorithm
    - Play on Russian Peasant Algorithm (invented by Egyptians) "how are these uneducated people doing math so fast?" (mathematician touring russia)
    - Registry in computer science comes up a lot
    - Toy implementation of RCA in talk
    - Observed that the knowledge the tickets are in sequential order is a relationship you can exploit. 
        - Is that relationship encodable? Imagine a Dafny style system. Hard to encode, but not impossible.
    - Why wouldn't size_t overflow? You don't have enough time to do it.
        - Why is a UUID of 128 bits enough to uniquely identify an object? It's enough to label every atom in the universe.
    - Alex S. believes infinities are wrong - insofar as they explain reality. The universe seems bounded both at the large and small. There's no infinite fast, there's no infinite time. There was a beginning, there's an end. The limits seem to be somewhere not much bigger than 128 bits. 
        - Even with uncertainty principle, there's a fundamental limit on our ability to observe. You can know location or speed, but not both. 
        - There seems to be a fundamental number of bits of knowledge that we can extract from anything. 
        - We're bounded by our own sensors, and our own speed of perception. 
            - When doing interactive software, we're always aware of the limits of human perception. There's a finite number of bits between which we can perceive differences. There's a limit on our physical resolution. 
        - We think we can perceive faster than we do, because we can predict. 
        - And this is a relationship we can exploit! We often overestimate how quickly we need to do animations, we just need to give the brain enough information to predict and see the

- Computers are a physical entity, governed by physics. They are finite in performance, memory, behavior. We tend to program as if it's abstract, but it's a physical entity. 
- Locality matters because locality matters from a physical standpoint. When things are close together in memory, the address of the space corresponds to the physical hardware. Cache locality is literally physically closer to the CPU, and saves time. This is a commonly accepted idea, could be a good starting place.
    - This breaks down because the computer always tries to predict your next move. If you break that and violate expectations, it's a cache miss and everything slows down. 
    - People still tend to write code as if random access is equally fast. But going out of sequence can be two orders of magnitude slower. 
    - Dabs shared a paper on encoding locality inside the mathematics of computer science. 
        - Response: we're struggling enough to encode things without locality!
    - As if our physicists ignored friction and we're trying to build cars.
    - The best we can do is point out the topic (in data structures) and in Sean's career alone we've moved beyond linked lists (because we didn't have caches when he started). There's really no reason to ever use a linked list. Yes, they're constant time insertion, but you're forgetting the linear time find-where-to-insert.
    
> "Names should not be associated with semantics because everybody has their own hidden assumptions about what semantics are, and they clash, causing comprehension problems without knowing why. This is why it's valuable to write code to reflect what code is actually doing, rather than what code "means": it's hard to have conceptual clashes about what code actually does."

///

- Relationships are a way to approach problems
- There's an analogue in writing - the five W's. We have a similar approach to engineering
- What are your entities? 
    - Philosophically, do these even exist? They exist insofar as they're useful for describing behavior. 
- What are the relationships? How do the entities relate to one another?
- Do these relationships have a name? Is this a common relationship that has a well known name, like "implication"?
- Connecting it to the existing body of work
    - meaning, "human knowledge" - math, human-to-human interaction, human-to-object interaction. English language. 
- I am the caller of the function, both functions are entities. The relationship are the pre- and post-conditions, aka a contract. 
- Usually they do have a well-defined name. If they don't, think about it more. If you've truly identified a fundamentally new type of relationship - 


## TODO
- [ ] Watch all of the Better Code talks and extract outlines
- [ ] Extract outline and glossary from [Sean's Github](https://github.com/sean-parent/sean-parent.github.io/blob/master/better-code/05-concurrency.md)
- [ ] 