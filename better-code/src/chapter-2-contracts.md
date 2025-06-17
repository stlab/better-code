# Contracts

Contracts are the connective tissue of solid software.  You really
can't build software at scale without them.  If you *are* building
large software systems, I promise you, you're using contracts, even if
you don't use that word for them, and I hope it'll be useful to deepen
your understanding of what you're already up to.

## Agenda

- Correctness
- Local reasoning
- Design by Contract
- Contract style

## Introduction

Fundamentally, contracts are about correctness.  Some people think
it's futile to pursue correctness, but I disagree, for three reasons:

First, it's more practical than you might think.  This doesn't mean
you'll reach a point where all bugs vanish, but you can reach a point
where you have well-justified confidence in the correctness of your
own work while maintaining high productivity… as long as you're not
measuring productivity in LOC.

Second, Simplicity.  The discipline we're talking about actually
removes tons of uncertainty and needless complexity from your code and
from the process of coding.  That's a big part of why I say it's
practical.

Last, it's just way more fulfilling to have a clear sense of when
you've done a thing right, and that doing the right thing is even
possible—than it is to “iterate until it seems to work.”

In case this wasn't clear, I'm saying that strong contracts make code,
and coding, simpler.  And I hope to demonstrate that through the
course of this seminar.I want to be clear, though, when I talk about
correctness, I don't mean some kind of elaborate formal proof. I mean
achieving correctness through the sort of everyday thinking that we do
while programming:


```swift
var names = [ "Sean", "Laura", "Dave", "Crusty" ]
names.sort()
print(names[3])
```

How do I know that last line is OK?  “I started with values in indices
zero through three sorting rearranges items without changing the
length so in the last line, I can still access item 3.”

Not to overly aggrandize this, but that's just an informal proof. So
regular programming is on the same continuum as formally proving
correctness and I'm going to inject a little more formality here. Not
as an academic exercise, but because it's practical and useful.

That kind of everyday thinking is only practical if we can reason
locally about code.  Here's what I mean: The clearest definition I've
found is this one from Nathan Gitter: “Local reasoning is the idea
that the reader can make sense of the code directly in front of them,
without going on a journey discovering how the code works”

So in our example, what we know about sort allows us to reason about
its use without looking at its implementation.

My brain has limited capacity. And I've found a lot of other peoples'
brains are limited too. Not yours of course, but a lot of peoples'
are. People like me can't keep the whole program in our heads, so we
do what humans always do when faced with complexity: we break
complicated problems into parts that can be understood in isolation.In
fact, local reasoning is so fundamental that most of our programming
best practices are there just to enable it.  It's why we make data
members private, why we break programs into components like functions,
types, and modules, and we try to keep them small.

## Hoare Logic

This discipline started with something called Hoare Logic, which the
British computer scientist and logician Tony Hoare first proposed in
1969.

He used this notation:

> {P}C{Q}

meaning that if precondition P is met, executing C establishes
postcondition Q

So for a trivial example, if x is less than the maximum integer,
incrementing x will leave it greater than the minimum integer

> {x < Int.max}  x+=1  {x > Int.min}

If you're allergic to formal notation, look away and just listen to my
words for a moment.

What makes preconditions and postconditions useful is this composition
rule: if the postconditions of one operation imply the preconditions
of the next one, and the first operation's preconditions are
satisfied, you can execute them in sequence and establish the
postconditions of the second operation.

> {P}C{Q} ∧ {P'}C'{Q'} ∧ (Q ⇒ P')  ⇒ {P}CC'{Q'}

This is just a formalization of the reasoning we use when we write
straight-line code, so our everyday programming practice is actually
well-founded. Not all code runs in a straight line, though, so Hoare
also gave us a tool for reasoning about loops.

A loop invariant is a condition that holds before and after each
iteration.  So in this linear search there's an invariant that no
element preceding the `i`th one is equal to `x`.

```swift
var i = 0
while (i != a.length && a[i] != x) {
  i += 1
}
```

Knowing that's upheld when the loop exits allows us to conclude that
the it finds the first x if there is one… not just any x.

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

Anyway yes, this is a talk about documentation. While it is true that
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
API to somebody.  The tower of abstraction mentioned earlier comes
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
More on all this in part 2.


You may have heard that some languages have features to support Design
by Contract.  In general, that means you can write *parts* of your
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
runtime. But there are two caveats:

1. **Contracts are fundamentally documentation**, even if they're
   expressed in code, so they must appear in the API descriptions
   consumed by client programmers. If you're using automated
   documentation extraction tools make sure they expose the contract
   code along with the API.

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
fragment that minimally describes what the thing is or does. That is
the first and most important part of the contract.  If you ask me for
a code review and every declaration outside a function body doesn't
have one of these summaries, I'm sending it back.

So this first one gives us the context we need to understand the
methods: we're looking at the declaration of dynamic array type that
holds any number of Ts.  Now let's look at the contract for the first
method, called "popLast."  As you can see from the summary, it removes
and returns the last element Notice that the phrase “last element” is
meaningful only because we documented that this thing is a collection,
which is a sequence of elements.  This method is a little unusual in
that it mutates the array and has a result, which means you need to
decide what to emphasize in the summary: the removal or the returned
value.  Here we've emphasized the mutation, which is normally what you
want.  You'd generally only emphasize the return value if the mutation
is something incidental that doesn't affect the program's meaning,
like updating a cache.

So let's spell out the preconditions, postconditions, and invariants
of this function.

What are the preconditions for removing an element?  Obviously, there
needs to be an element to remove.This means a client of this method is
considered to have a bug unless the array has an element.  OK, so what
about postconditions?



The postcondition is the effects the method has, plus any returned
result.  If the preconditions are met, but the postcondition isn't,
we'd say the method has a bug.  The bug could be in the documentation
of course; that's part of the method.

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

Because I've validated that the invariant is implied, I'm going to
erase that too.In fact, the precondition is sort of implied by the
summary too.  You can't remove and return the last element if there's
no last element, right?

Whether or not to omit an implied precondition may be a slightly
different judgement from the others. Because it's information every
client needs in order to not have a bug, it might be a good idea to
spell it out.  This is a method of Arrays that sorts the elements
according to some comparison predicate `areInIncreasingOrder`.  So if
we pass it the less-than operator, which is true when the first
argument is less than the second, we get the elements arranged from
least to greatest.  The summary gives the postcondition that no two
adjacent elements are out-of-order according to the predicate.  I
apologize for the weird negative phrasing of the postcondition, but
there's no other way to say it given the need to handle equal
elements, for which the predicate will return false.  That's a little
tricky, but not really important to this presentation, so if it's not
clear to you yet, let's talk about it afterward.

In fact, I don't normally clutter up my documentation with examples,
but because it's tricky, this is a case where an example might really
help Anyway two things to notice here:First, there's an explicit
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

Which brings me to this aside…  A big part of making the documentation
problem tractable is having some well-chosen project-wide policies
that save you from repeating common patterns. So I'm not going to
prescribe your project's policy about this, but you should choose one,
and write it down somewhere.  Your project's choice of policy can make
the difference between documentation being useful and being burdensome
or inconsistent (at which point people will just stop reading and
writing it).

>> Note that it is fine to put information in the policies without
which the project's other documentation would be incomplete or
confusing.  For example, this says that every function that cannot
throw an exception is declared or documented as such.  I want to
mention one other thing: everything you see in these function
signatures is implicitly part of the function's contract. For example,
the signature says the predicate must operate on arguments of type T,
and return a `Bool`, so we didn't have to spell that out as a
precondition in documentation.

Because Swift is a statically typed language, it just so happens that
those things are going to be enforced by the compiler, but if you're
programming in a totally dynamic language, like Javascript, or Python
without type hints, you have to put a lot more of that information
into the written documentation.

Okay, now let's talk about errors.  So we already talked about bugs as
faulty code, resulting in a failure to satisfy preconditions or
postconditions.  If we detect one of these conditions, in general,
there's no way to know where the bug is or how much damage has been
done to the program's supposed invariants: it could be "in a bad
state."  The bug may have been in the very code that was responsible
for maintaining that state.  That's why diagnosing and fixing bugs is
hard!

An error is not-that.  When there's an error, no code is at fault, but
the postcondition can't be satisfied.

For example, you can't save a document if the disk is full, and you
may not be able to load a document from disk if the data turns out to
be corrupted.  In these cases the program state is still okay, and the
client might have a reasonable way to recover and continue running.
Sometimes this just means reporting the error to the user and waiting
for the next command.

>> So only the neeedless postcondition violations are bugs.Let's
>update our sorting function to deal with a comparison that can report
>errors.  Maybe the comparison needs to allocate space on disk or
>something.

In Swift we'd do that by making the comparison a throwing function.
And then we have to say that sort can throw if the comparison can
throwIn Swift, if something is going to throw, you have to declare
that fact explicitly, If you're stuck with a language like C++,
Python, or Java that doesn't make you put error information in the
signature, you have to find another way to document it for client
coders.

In those cases I normally have a policy that by default, anything can
report an error, and say that operations that will never report errors
must document that fact.

Because we said an error represents a failure to meet postconditions,
the postcondition doesn't tell you anything about the the state of the
program when an error is reported.  But if you really don't know
*anything* about the state of the program, you probably can't recover.

Fortunately, we can assume by default that a failing operation only
mutates the things it would mutate in case of success.

So in the case of `sort`, we know the array was mutated… somehow, but
we don't know much more than that.  Is there anything more we can
reasonably guarantee in case of an error?

You might think, it's _possible_ that our clients could do something
with the array if they know that the array is still a permutation of
the original elements, just rearranged, but I want to caution you
against the line of thinking that goes, “it's *conceivable* that some
unknown client may have a use for this feature or guarantee, so I'm
going to give it to them.”

1. It's very hard to retract once it's given, because you may break
   code.
2. The guarantee complicates your contract: it needs to be described;
   potential clients need to read and understand it.
3. The guarantee is likely to complicate your implementation and your
   tests.
4. Making needless guarantees may constrain the implementation in ways
   that rule out the most efficient implementation, now or in the
   future.

In general, describing a partially mutated state is complex, probably
not useful, and may be impossible. So clients need to assume values
under mutation have arbitrary meaningless values after an error is
reported.

This is not as useless as it sounds at first: there's a good chance
they're on the stack and will be destroyed when the scope exits.  And
if you work on a desktop application with undo, it's effectively
saving a snapshot of the document before every mutation, so your
program is very likely set up to discard partial mutations of
important state.

So this is the theory of error handling I developed back in 1998 for
the C++ standard library.  It says that there are 3 useful kinds of
promises an operation can make with respect to errors.

The minimum guarantee is this basic guarantee that invariants are
always upheld, the idea being that we don't know how to reason about a
program if broken invariants are visible outside a type's
encapsulation boundary.

The next stronger guarantee says that if an error is reported, the
operation has no observable effects; it's transactional

And then the strongest guarantee an operation can make is that it
won't report any errors at all.  You need a no-error guarantee from
any operations used in error recovery, or you end up with some kind of
infinite recovery recursion.  I told you that you can lean on
invariants for reasoning, so you might find the idea of an
interrupted, partial mutation alarming, because that could leave
invariants broken.  That collection of pairs offers a good example, if
appending an element to a vector can fail, as in C++

Now I realize that lots of modern programming languages treat
out-of-memory as something that can't happen, so if you use one of
those languages, imagine that the private arrays in this thing are a
different type, `DiskVector`, that's backed by storage on disk, and we
can run out of disk space trying to grow them.

If an error occurs trying to do the second append, as coded, we're
left with a broken invariant, because the length of `xs` is one
greater than the length of `ys`.

So how could we uphold the invariant? There are a number of
strategies.

Here's one totally legit way.

If anything fails, we just discard all the elements.  This is what we
call the Basic Error Guarantee: it says that all invariants are upheld
and nothing is leaked.

This is a nice place to land because the instance of `PairVector` is
still in a good state, and its operations still function as normal.
On the other hand, even if the invariant is upheld, from the client's
perspective this is still a partially mutated object with a
meaningless value, and we really shouldn't be doing anything with it.
We'll come back to that.

By the way, we need to know something in order for this method to give
the basic guarantee: it only works if `clear()` can't fail—if it gives
the nothrow or nofail guarantee.  Remember I said that whether an
error can occur is part of an operation's contract?  It's crucial
information because error *recovery* needs to use operations that
can't themselves report errors.

In contrast, which specific errors can be reported is comparatively
unimportant except for the very lowest level primitives, because
there's usually just one strategy for error recovery.  And remember,
if you try to spell that information out and your clients don't need
it, you've fallen into the trap of giving premature guarantees.It
turns out that `push_back` can give a stronger guarantee than the
basic one if we recover this way:

>> If the second `push_back` fails, we just undo the first one and the
>`PairVector` is unchanged.  >>

The strong guarantee that an operation either succeeds or has no
effects is actually useful to clients in practice, unlike most
statements describing partial mutations.It's also very simple to
describe, so it doesn't overly complicate the specification.

In fact, we're taking advantage of the strong guarantee from
`vector`'s own `push_back` method hereit's why no recovery is needed
if the first `push_back` failsand it's why the catch block only needs
to adjust `xs`: because we know that if we get there, `ys` is still
unchanged.

So this is nice.  Should all operations give the strong guarantee?
Let's look at sort

Pretty much the only way to get the strong guarantee here is to use
what I call a "copy and swap" strategy.

First we make a copy of the thing under mutation, then we try to do
the mutation on the copy, and only if everything works out, we swap
the original for the copy.

This approach leaves `self` unmodified if `actuallySort` fails.  But
it's super expensive: it allocates memory, and incurs O(N) space and
time overhead.  Since we're not sure every client of `sort` needs the
strong guarantee, we shouldn't force them to accept this expense.
It's a form of giving away the store.

On the other hand, the strong guarantee makes sense for `PairVector`'s
`push_back` because it's achievable without loss of efficiency. It
even falls out of maintaining invariants in the most natural way.

What you've seen so far is basically the theory of error handling that
I developed back in 1998 for the C++ standard library, with every
operation being required to give at least the Basic Guarantee, because
the idea that invariants must always be maintained is sort of
foundational. It's a tried and true way to approach thinking about
errors and correctness.  But I'd be remiss if I didn't describe Sean's
2022 update to the theory which he calls “error handling the other way
around.”

It's based on the insight that an unknown partially-mutated value is
meaningless, so any operations you do on it, other than destruction
and maybe assignment, represent a bug—also known as nonsense.
Remember if the client uses an operation in a buggy way, the ethos of
blame says the operation has no obligations.

So Sean's thesis is that when an operation can't efficiently give the
strong guarantee, maybe upholding invariants is a waste of effort,
because further operations on the value are all bugs.

It's the client's obligation to discard any partially mutated value
via destruction or assignment, so all we really need to do is leave
the partially-mutated object in a destructible and assignable state.

In my 1998 theory of error handling, type invariants are required to
hold after every public operation, whether an error is reported or
not.  If we do error handling “the other way around,” they're only
required to hold if the operation is successful or if it gives the
strong guarantee.  Whichever policy you choose—you got it—write it
down in your policy document.  You own a supercar, a $8M Bugatti Divo.
This thing has extremely tight tolerances, basically to be “in a good
state” you have to care for it properly and maintain its invariants.
Therefore you've got a contract with an ultra-exclusive "car butler"
who takes care of all the maintenance, including refueling.  The
contract, of course, says the butler is only going to use
ultra-premium gas.  One day you get a notice from the state that says
it's time to come in for a smog check. You have your assistant drive
take the car in and you find out the car violates the precondition for
continued operation.  You take the car back to the dealer and they
tell you the engine is shot and now the car is valued at only $2M,
practically worthless.  How did this happen?!  You ask the dealer to
investigate, so they do a whole battery of tests and the only thing
they can find is that the car's tank is full of economy gas like you'd
use in a Prius.  Your butler, clearly, had a bug, and the wrong fuel
has been eating away at the valves and piston heads for months.  You
never really push the car too hard, so you don't notice any difference
in performance, but the damage is done.
