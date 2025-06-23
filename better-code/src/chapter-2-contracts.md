# Contracts

Contracts are the connective tissue of solid software.  You really
can't build software at scale without them.  If you *are* successfully
building large software systems, you're already using  contracts in
some form, and this chapter should help you make them more powerful.

## In pursuit of Correctness

Fundamentally, contracts are about the first ingredient of Better
Code: correctness. Some folks write off the pursuit of correctness,
because bugs are inevitable, and in practice, and we rely on incorrect
software every day without disaster (for the most part). But that
approach throws out the baby with the bathwater.  There is a practical
approach to correctness that improves both code quality and the
programming experience, without demanding unrealistic perfection.

For those who like to think formally, we can define a _semi-correct_
program as one for which there exists a valid initial state and
inputs, such that the program will generate a valid output. As an
analogy, a broken clock is semi-correct, it is correct twice a
day. This definition provides a partial ordering of correctness, where
a program is _more correct_ than another if the initial states under
which it is correct are a superset of the other.

So while you may not reach a point where all bugs vanish, but you will
have well-justified confidence in the correctness of your own work
while maintaining high productivity. Also, the discipline we'll
describe here of **programming by contract** removes uncertainty and
needless complexity from your code and from the process of coding.
That's a big part of why we say it's practical.

## Reasoning about correctness

How can you know whether your program is correct?  Validating
correctness seldom requires an elaborate formal proof—usually the sort
of everyday thinking that we do while programming suffices.

```swift
var names = [ "Sean", "Laura", "Dave", "Crusty" ]
names.sort()
print(names[3])
```

In the example above, how do we know that last line is OK? Our thought
process is something like this:

- We started with values in indices zero through three of `names`.
- sorting `names` rearranges elements without changing the set of valid indices.
- Therefore, in the last line, `names` still has an element at index `3`.

That's just an informal proof, and we use that kind of reasoning every
time we write a line of code. So regular programming is on the same
continuum as formally proving correctness.  We're going to explore the
power that's available by moving toward the formal end of that
spectrum to see how it enables Better Code.

## Local Reasoning

The kind of everyday thinking demonstrated above is only practical if
we can reason locally about code.  The clearest definition of Local
Reasoning we've found is [this
one](https://medium.com/@nathangitter/local-reasoning-in-swift-6782e459d)
from Nathan Gitter: “Local reasoning is the idea that the reader can
make sense of the code directly in front of them, without going on a
journey discovering how the code works.”

So in our example, what we know about `sort` allow us to reason about
its use without looking at its implementation.  In fact, local
reasoning is so fundamental that most of our programming best
practices exiast just to support our ability to do it.  It's why we
use access control, why we break programs into components like
functions, types, and modules, and why we try to keep them small.

## Components and Abstraction

Obviously, “knowing something about `sort`” is only possible and
relevant because `sort` is a separate component with its own name. If
we had injected the sorting implementation directly into our code,
we'd have to reason about all of its details, and we'd need a comment
to tell us that the implementation was sorting the elements.

So it's a common fallacy that factoring out a component only makes
sense if it's used more than once. The real criterion is whether you
can identify a unit of *abstraction*—the third ingredient of Better
Code.  If you can think of a simple and descriptive name for
something, that's usually a good indicator that there's an abstraction
waiting to be discovered.

In fact, creating a component directly creates the opportunity for an
additional use site: in testing.  The more code you test separately,
the better it is for correctness.  The more you can use understandable
abstractions, the simpler and clearer the use-sites become, which is
better for correctness. Abstraction and correctness support one
another in a virtuous cycle.  And abstraction is necessary for
programming at scale: because can't keep the whole program in our
heads, we do what humans always do when faced with complexity: we
break complicated problems into parts that can be understood in
isolation.

## Hoare Logic

Programming by contract grew out of Hoare Logic, developed in 1969 by
the British computer scientist and logician Tony Hoare.  While we
won't be using Hoare Logic directly, we'll discuss it briefly to
provide historical context, and because it is the source of crucial
terminology.

### Preconditions and Postconditions

Hoare used this notation, called a “Hoare triple,”

> {P}S{Q}

which is an assertion that if **precondition** *P* is met, operation
*S* establishes **postcondition** *Q*.

For example:

- if we start with `x == 2` (precondition), after `x += 1`, `x == 3` (postcondition):

  > {x == 2}x+=1{x == 3}

- if `x` is less than the maximum integer (precondition), after `x
  += 1`, `x` is greater than the minimum integer (postcondition):

  > {x < Int.max}x+=1{x > Int.min}

What makes preconditions and postconditions useful for formal proofs
is this composition rule:

> {P}S{Q} ∧ {Q}T{R} ⇒ {P}S;T{R}

Given two valid Hoare triples, if the postconditions of the first are
preconditions of the second, we can form a new valid triple describing
the effects of performing the operations in sequence.  The notation
may look exotic, but its meaning should be familiar: this rule simply
captures the reasoning we use to think informally about statements
when we write straight-line code.

### Invariants

Not all code runs in a straight line, though, so Hoare
also gave us a tool for reasoning about loops.

A **loop invariant** is a condition that holds before and after each
iteration.  In this linear search there's an *invariant* that no
element preceding the `i`th one is equal to `x`.

```swift
var i = 0
while (i != a.count && a[i] != x) {
  i += 1
}
```

Knowing that's always true when the loop exits allows us to conclude
that if `i != a.count`, the *first* occurrence of `x` in `a` is at
index `i`.  Anything else would contradict the loop invariant.

## Design By Contract

> *…a software system is viewed as a set of communicating components
> whose interaction is based on precisely defined specifications of
> the mutual obligations — contracts.*
>
>   —Building bug-free O-O software: An Introduction to Design by Contract™
>    https://www.eiffel.com/values/design-by-contract/introduction/

So enough formalisms. In the mid 1980s, The French computer scientist
Bertrand Meyer took Hoare Logic, and shaped it into a practical
discipline for software engineering that he called “Design By
Contract”

He describes contracts as the precise specification of mutual
obligations between interacting software components.

So contracts describe the rules that govern how one piece of software
talks to another. In other words, they're relationships.  Thinking in
terms of relationships is one of the themes of Better Code, and you
can expect us to point relationships out as they come up in our
material.

Contract: specifies the relationship between an operation and the clients that invoke it.

The basics of design by contract should look familiar; they come
straight from Hoare:

- an operation's preconditions—the obligations of a correct client
- its postconditions—the obligations of the operation when correctly called
- its invariants—what is true both before and after the operation

Meyer added two key ingredients to Hoare's work.  An ethos of blame.
Now that might sound like something you want to eliminate from your
programming culture, but this applies to code, not people.

If preconditions don't hold, that's a bug.  The client code is at
fault, and the operation is not required to make any promises.

If preconditions hold but postconditions are not fulfilled, that's a
bug, and the operation's code (or something it calls) is at fault.

Being able to say which code is at fault is extremely powerful! You
know which code to fix; It's simplifying and clarifying.

And if you ever find yourself with something that's clearly a bug but

you can't decide which code to blame, that's a sign that a contract is
missing or incomplete.

> If software malfunctions and you can't clearly assign blame, a
> contract is missing somewhere.

A system that exposes these situations, where everybody is playing by
the rules but things still go wrong, is called a footgun.

## Type Invariants

The most important contribution of Meyer's Design by Contract was to
apply the idea of “invariants” to user-defined types with private
parts.

Meyer's *class invariant* (or *type invariant*), is a condition that
holds at the boundary between a type's public API and its
implementation detail.

just a formalization of what we mean when we talk about instances
being “in a good state.”

- Condition that holds whenever a type interacts with clients.
- “It's in a good state” ≅ the invariant is upheld

### Example:

My favorite example is this type that holds a pair of private arrays
but whose public interface is more like an array of pairs.  The
invariant for this type is that the private arrays have the same
length.


```swift
/// A random-access collection of `(X, Y)` pairs.
struct PairArray<First, Second> {
  /// The first part of each element.
  private var xs: [X] = []

  /// The second part of each element.
  private var ys: [Y] = []

  /// An empty instance.
  public init() {}

  /// The `i`th element.
  public subscript(i: Int) -> (X, Y) {
    (xs[i], ys[i])
  }

  /// The length.
  public var length: Int { xs.length }

  /// Adds `e` to the end.
  public mutating func append(_ e: (X, Y)) {
    xs.append(e.0)
    ys.append(e.1)
  }
}
```

It's important to realize that to be a class invariant, the condition
only needs to hold at the public interface boundary; it's perfectly
fine to violate the condition when no clients can observe it.  In
fact, it's necessary during a mutation.  If we want to add a new pair,
we have to grow one of these vectors first, which breaks the invariant
until we've done the other push_back.  That's not a problem because
the vectors are private and we encapsulate the invariant inside a this
public method, that appends a pair.  By the time that method returns,
everything is back in order.

The beauty of having public and private access control is that it
doesn't take much attention to uphold a type invariant.  The condition
needs to be established the constructor, and an operation that mutates
private parts needs to restore the condition, and that's it!

Non-mutating operations can't disturb the invariant, and mutating
operations that only use the public API are in the clear too.  This is
a really trivial example, but having this strong invariant simplifies
the code that computes the length of the PairArray.  We don't have to
take the minimum of two lengths, because we know the lengths are
equal.

### Spoiler Alert: It's Documentation

> All undocumented software is waste. It's a liability for a company.
>
> —Alexander Stepanov (https://youtu.be/COuHLky7E2Q?t=1773)

Looking back at Meyers' definition, you might notice he says contracts
are “precisely defined specifications,” which is just a fancy word for
documentation.

Now, lots of people think documentation is a waste of time, but if
you've been to any of my talks you know that I don't agree.  Somehow I
always seem to end up talking about this. If you're going to be in the
correctness game, you need documentation.  Correctness is always with
respect to a specification, so undocumented software is neither
correct nor incorrect.

>> In fact, I don't review code; I review contracts… or at least, I
>review contracts first.  If you ask me for a code review and there's
>anything without contract documentation, I'll reject it, because
>there's no way to make a judgement about its correctness.

And then, if the contracts aren't well-specified and designed, I'm not
going to bother looking at the implementation.  Remember, the
contracts are the connective tissue; they're what every client of a
component interacts with; they will have effects throughout the
codebase.  The implementation, well, that had better be an expression
of the contract, but that's, like… the final detail.

Anyway yes, contracts about documentation. While it is true that
there are lots of counterproductive approaches to documentation, I'm
going to show you one that is practical *and*—if you give the process
the attention it deserves—can help you improve the code of your APIs.
I also want to point out that documentation is essential for local
reasoning.  It's the reason I don't need to be a condensed matter
physicist to program a computer.

Here's what I mean. As programmers, we're working on what my friend
Sam Lazarus calls “a tower of abstraction” that stretches through the
libraries and programming language we use, the operating system, and
into the hardware, which ultimately rests on the laws of physics.

So what keeps us from recursing down to the limits of known physics
when we think about how our programs work?

The answer is documentation.  We can use libraries and our programming
language without digging into their implementations because there's a
solid spec.  The compiler backend engineers can do their jobs because
the hardware manufacturers document the architecture and instruction
sets. The hardware designers succeed because the physicists document
the laws of physics.  That's the tower, and you're a part of it.  The
bad news, of course, is that you're not at the top of the
tower. Someone else, or future-you, is going to have to build on the
code you're writing.  That means there's no difference between public
and private stuff where documentation is concerned.  Everything is an
API to somebody.

### A Tower of Invariants

The tower of abstraction mentioned earlier comes
with a tower of invariants.  The invariants of the type with the two
arrays in it are built on—and depend on—the invariants of the
individual arrays, and you could embed this type into some larger data
structure with its own invariant.

In fact, you can think of the entire state of your program as one big
data structure with its own invariants, and formalize what it means
for the program to “be in a good state” that way.  For example,

- you might have a database of employees, each with
- an ID of its own
- a manager ID (The CEO gets to be his own manager)

It's an invariant of your program that a manager ID can't just be
random; it has to identify an employee that's in the database—that's
part of what it means for the program to be in a good state, and all
through the program you have code to ensure it's upheld.  It would be
a great idea to identify and document that whole-program invariant.

### Encapsulating invariants

An even better idea is to use *encapsulate* the invariant in a type,
and document _that_.  So instead of using an `SQLDatabase` type
directly, maybe create an `EmployeeDatabase` type with a private
`SQLDatabase`, whose public API always upholds that invariant.  Now
you can remove that logic from the rest of your code.  This is one of
the most powerful transformations you can make.

```swift
/// The employees of a company.
///
/// Invariant: every employee has a manager in the database.
struct EmployeeDatabase {
  /// The raw storage.
  private var storage: SQLDatabase;

  /// Adds a new employee named `name` with manager `m`, returning the
  /// new employee's ID.
  public addEmployee(_ name: String, managedBy m: EmployeeID) -> EmployeeID

  /// Removes the employee identified by `e`.
  ///
  /// - Precondition: `e` identifies an employee who is not the
  ///   manager of any other employee.
  public remove(_ e: EmployeeID)

  ...
}
```

Upholding invariants is the _entire purpose_ of access control, so use
that whenever you can!  Lastly, I want to say, this documentation should
go in your code as comments, because:

1. That puts the two things that should correspond—documentation and
   implementation—next to one another, so you can see when they don't
   match up. People sometimes complain that docs go out of date, but
   that's kinda the point: without the ability to see that
   inconsistency, there's no way to know that there's a bug.

2. Using comments makes it reasonable to combine the activities of
   coding and documentation, which—believe it or not—are mutually
   supportive.

But if we're going to integrate documentation into our programming so
tightly, we need to make sure it's neither intrusive for the
maintainer to read nor burdensome for the author to write.  Ideally,
it should help both of them.  Just to give you an idea that it's
practical, though, this example we saw earleir has what I consider
minimal but complete contract documentation for each declaration.

Now, not every contract is as simple as these are, but simplicity is a
goal.  In fact, if you can't write a terse, simple, but _complete_
contract for a component, there's a good chance it's badly designed.

You may have heard that some languages have features to support “Design
by Contract.”  In general, that means you can write *parts* of your
contracts as code, and get some checking at runtime to make sure these
contracts are upheld.

```swift
struct MyArray<T> {
  ...

  // Returns the `i`th element.
  @requires(i >= 0 && i < self.count)
  fun getNth(i: Integer): T

  ...
}
```

The idea started with Bertrand Meyer's own Eiffel language, and was
picked up by many others, including D, Scala, Kotlin, and
Clojure. Other languages, like Rust and Python, have contract
libraries that provide a near-native contract programming experience.

If you use one of these languages, fantastic; *absolutely do* leverage
those features and libraries.  That can reduce the amount of pure
documentation you need to write and add automated contract checking at
runtime. But there are caveats:

1. **Contracts are fundamentally documentation**, even if they're
   expressed in code, so they must appear in the API descriptions
   consumed by client programmers. If you're using automated
   documentation extraction tools make sure they expose the contract
   code along with the API.  If not, you need to repeat the complete
   contract in documentation.

2. Some contracts are better expressed in English than as code,

3. Some contracts are impossible to express as code.  We'll
   see an example in a moment.

```swift
/// A resizable random-access collection of `T`s.
struct DynamicArray<T> {

  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }

  /// The `i`th element.
  public subscript(i: Int) -> T { ... }

  /// The length.
  public var length: Int { ... }
    .
    .
    .

  /// The number of elements that can be stored before storage is
  /// reallocated.
  private var capacity: Int { ... }
}
```

So the first thing to notice about this code is that the method bodies
are collapsed, because this is not about what you put in your
implementations.  Contracts are part of your function's interface.

The only time we're going to look into method bodies today is when we
talk about programmatic checking, and only when the language forces us
to do it in the body; otherwise it's all about interfaces.  Next
notice that every declaration here has a summary, which is a sentence
fragment that minimally describes what the thing *is* or *does*. That is
the first and most important part of the contract.  If you ask me for
a code review and every declaration outside a function body doesn't
have one of these summaries, I'm sending it back.

The first one

```swift
/// A resizable random-access collection of `T`s.
struct DynamicArray<T>
```

gives us the context we need to understand the
methods: we're looking at the declaration of dynamic array type that
holds any number of Ts.  Now let's look at the contract for the first
method, called "popLast."

```swift
  /// Removes and returns the last element.
  public mutating func popLast() -> T { ... }
```

As you can see from the summary, it removes and returns the last
element. Notice that the phrase “last element” is meaningful only
because we documented that this thing is a collection, which is a
sequence of elements.  This method is a little unusual in that it both
mutates the array and returns a result, which means you need to decide
what to emphasize in the summary: the removal or the returned value.
Here we've emphasized the mutation, which is normally what you want.
You'd generally only emphasize the return value if the mutation is
something incidental that doesn't affect the program's meaning, like
updating a cache.

So let's spell out the preconditions, postconditions, and invariants
of this function.

What are the preconditions for removing an element?  Obviously, there
needs to be an element to remove.

```swift
  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  public mutating func popLast() -> T { ... }
```

This means a client of this method is considered to have a bug unless
the array has an element.  OK, so what about postconditions?

The postcondition is the effects the method has, plus any returned
result.  If the preconditions are met, but the postcondition isn't,
we'd say the method has a bug.  The bug could be in the documentation
of course; that's part of the method.

```swift
  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Postcondition: The length is one less than before
  ///   the call. Returns the original last element.
 public mutating func popLast() -> T { ... }
```

And what's invariant here?  The rest of the elements are unchanged.
Now, if the postcondition seems a bit glaringly redundant with the
summary, that should be no surprise.  The summary of a method should
describe what the method does, and what it should return.  That's
basically the postcondition.

So the postcondition will very often not be stated separately from the
method's description.  The only reason you might write it out is if
there's some aspect of the postcondition you can't easily capture in
the summary.

I'm going to erase the postcondition now, but it's important to ask
yourself what the postconditions are and make sure they're completely
captured by the summary before you do this.  Considering the
postcondition is part of the process that makes the summary complete.

And if we know everything the method does is captured in the summary,
we can assume everything else in the program is unchanged, so the
invariant is also trivially implied.  And that is also very commonly
omitted.

```swift
  /// Removes and returns the last element.
  ///
  /// - Precondition: `self` is non-empty.
  /// - Postcondition: The length is one less than before
  ///   the call. Returns the original last element.
  /// - Invariant: the values of the remaining elements.
 public mutating func popLast() -> T { ... }
```

Because I've validated that the invariant is implied, I'm going to
erase that too. In fact, the precondition is sort of implied by the
summary too.  You can't remove and return the last element if there's
no last element, right?

Whether or not to omit an implied precondition may be a slightly
different judgement from the others, because it's information every
client needs in order to not have a bug.  Regardless, a client must
assume that any condition required for the summary to make sense is a
precondition.  We recommend your project's policy only *requires*
precondition documentation where those preconditions are not obviously
implied by the summary.  In the end, the original declaration should
be sufficient:

```swift
  /// Removes and returns the last element.
 public mutating func popLast() -> T { ... }
```

This example shows that complete and precise documentation need not be
overly burdensome for the reader or the writer.

### A More Complicated Example

```swift
extension Array {
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1],
  /// self[i])` is false for each `i` in 0 ..< length - 1.
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering
  ///   over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
}

var a = [7, 9, 2, 7]
a.sort(areInIncreasingOrder: <)
print(a)     // prints [2, 7, 7, 9]
```

This method of Arrays that sorts the elements
according to some comparison predicate `areInIncreasingOrder`.  So if
we pass it the less-than operator, which is true when the first
argument is less than the second, we get the elements arranged from
least to greatest.  The summary gives the postcondition that no two
adjacent elements are out-of-order according to the predicate.  I
apologize for the weird negative phrasing of the postcondition, but
there's no other way to say it given the need to handle equal
elements, for which the predicate will return false.  That's a little
tricky, but not really important.

We don't normally clutter up our documentation with examples, but
because the statement of effects is tricky, this is a case where an
example might really help.

```swift
  /// Sorts the elements so that `areInIncreasingOrder(self[i+1],
  /// self[i])` is false for each `i` in 0 ..< length - 1.
  ///
  ///     var a = [7, 9, 2, 7]
  ///     a.sort(areInIncreasingOrder: <)
  ///     print(a)     // prints [2, 7, 7, 9]
  ///
  /// - Precondition: `areInIncreasingOrder` is a strict weak ordering
  ///   over the elements of `self`.
  /// - Complexity: at most N log N comparisons, where N is the number
  ///   of elements.
  mutating func sort<T>(areInIncreasingOrder: (T, T)->Bool) { ... }
```

Anyway two things to notice here: First, there's an explicit
precondition that isn't implied by the summary.  We require that the
predicate be a strict weak ordering, which is a set of properties we
need to make the the result meaningful. I'm not going to go over all
of those properties, but to see why it might be important, we can just
look at one of them: the property of stability. The predicate needs to
have a consistent result for any pair of argument values if you call
it multiple times. I hope it's obvious that we couldn't promise that
the result is sorted according to the predicate if the result of the
of the predicate were random.

Incidentally, this is one of those preconditions for which no test can
be written in code.  Second, I've documented the performance of this
method.  Time and space complexity have to be part of the contract if
you want your clients to be able to reason locally about the
performance of their own code.  The only reason you haven't seen
complexity documented in this talk up to now is that I have a policy
that operations have constant complexity unless specifically
documented otherwise.

### Project-Wide Documentation Policies

Which brings me to this aside…  A big part of making the documentation
problem tractable is having some well-chosen project-wide policies
that save you from repeating common patterns. So I'm not going to
prescribe your project's policy about this, but you should choose one,
and write it down somewhere.  Your project's choice of policy can make
the difference between documentation being useful and being burdensome
or inconsistent (at which point people will just stop reading and
writing it).

For example,

- Every declaration outside a function body must have a documentation comment that describes
  its contract.
  - Start with a summary sentence fragment.
    - Describe what a function or method does and what it returns.
    - Describe what a property or type is.
    - Separate the fragment from any additional documentation with a blank line and end it
      with a period.
  - Preconditions, postconditions and invariants obviously implied by the summary need not
    be explicitly documented.
  - Declarations that fulfill protocol requirements are exempted when
    nothing useful can be added to the documentation of the protocol
    requirement itself.

- End every file with a newline.
- Do not strip trailing whitespace from lines you're not editing; it creates spurious VC diffs.
- Document the performance of every operation that doesn't execute in constant time and space.


It is reasonable to put information in the policies without which the
project's other documentation would be incomplete or confusing, but
you should be aware that it implies policies must be read.


I want to mention one other thing: everything you see in these
function signatures is implicitly part of the function's contract. For
example, the signature if `sort` says the predicate must operate on
arguments of type T, and return a `Bool`, so we didn't have to spell
that out as a precondition in documentation.

Because Swift is a statically typed language, it just so happens that
those things are going to be enforced by the compiler, but if you were
programming in a totally dynamic language, like Javascript, or Python
without type hints, you have to put a lot more of that sort of
information into the written documentation.
