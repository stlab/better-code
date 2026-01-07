# Errors

In the *Contracts* chapter you may have noticed we made this reference
to the concept of *errors*:

> If the preconditions are met, but the postconditions are not, and
> the function does not report an error, we'd say the method has a
> bug.

In the interest of progressive disclosure, we didn't look closely at
the idea, because behind that simple word lies a chapter's worth of
discussion.  Welcome to the *Errors* chapter!

Before we get into it, we want you to know that what we present here
is not the only logically consistent approach to errors, and our
approach may clash with your instincts.  It is the result of
optimizing for local reasoning and scalable software development, and
the justifications for our choices are interdependent.  We hope you'll
bear with us as we tie them all together.

## Definitions

To understand any topic, it's important to define it crisply, and
unfortunately “error” and associated words have been used rather
loosely, and previous attempts to define these words have relied on
other words, like “expected,” which themselves lack clear definitions,
at least when it comes to programming.

Unless we want to invent new terms, we will have to impose a little of
our own structure on the usual terminology. We hope these definitions
are at least consistent with your understanding:

> **Error**: a condition in conflict with the primary intention of the
> code.

When we write the word “error” in normal type, we mean the idea above,
distinct from the related Swift `Error` protocol, which we'll always
spell in code font.

We'll divide errors into three categories:[^common-definition]

> - **Input error**: the program's external inputs are malformed.  For
>   example, a `{` without a matching `}` is discovered in a JSON
>   file.
>
> - **Bug**: code contains an avoidable[^avoidable] mistake. For
>    example, an `if` statement might test the logical inverse of the
>    correct condition.
>
> - **Failure**: a function could not fulfill its postconditions even
>   though its preconditions were satisfied.  For example, writing a
>   file might fail because the filesystem is full.

[^avoidable]: While bugs in general are inevitable, every *specific*
    bug is avoidable.

[^common-definition]: While some folks like to use the word “error” to
refer only to what we call *failures*—as the authors have done in the
past—the use of “error” to encompass all three of these categories
seems to be the most widespread practice. We've adopted it to avoid
clashing with common understanding.

## Error Recovery

Let's begin by talking about what it means to “recover from an error.”
[Perhaps the earliest use
](https://dl.acm.org/doi/10.1145/800028.808489) of the term “error
recovery” was in the domain of compilers, where the challenge, after
detecting a flaw in the input, is to continue to process the rest of
the input meaningfully.  Consider a simple syntax error: the simplest
possiblities are that the next or previous symbol is extra, missing,
or misspelled.  Guessing correctly affects not only the quality of the
error message, but also whether further diagnostics will be
useful. For example, in this code, the `while` keyword is misspelled:

```swift
func f(x: inout Int) {
  whilee x < 10 {
    x += 1
  }
}
```

As of this writing, the Swift compiler treats `whilee` as an
identifier and issues five unhelpful errors, four of which point to
the remaining otherwise-valid code.  That's not an indictment of
Swift; doing this job correctly is nontrivial.

<!-- The reference below is a Jul 15, 2016 stack overflow answer that
supposedly quotes an article at
http://javaconceptoftheday.com/difference-between-error-vs-exception-in-java/
but I have checked the wayback machine and can't find that phrase
anywhere on the page (nor anywhere else on the modern web, with
Google). The point is to capture the idea of invariants being
intact. -- DWA -->

More generally, [it has been
said](https://stackoverflow.com/a/38387506) that recovering from an
error allows a program to “to sally forth, entirely unscathed, as
though 'such an inconvenient event' never had occurred in the first
place.”

Being “unscathed” means two things: first, that the program state is
intact—its invariants are upheld so code is not relying on any
newly-incorrect assumptions.  Second, that the state makes sense
given the correct inputs received so far. “Making sense” is
a subjective judgement. For example:

- The initial state of a compiler, before it has seen any input, meets
  the compiler's invariants. But when an error is encountered,
  resuming with that state would discard the context seen so
  far. Unless the code following the error would have been legal at
  the beginning a source file, the compiler will issue many unhelpful
  diagnostics for that following code. Recovery means accounting
  somehow for the non-erroneous code seen so far and re-synchronizing
  the compiler with what follows.

- In a desktop graphics application, it's not enough that upon error
  (say, file creation fails), the user has a well-formed document; an
  empty document is not an acceptable result.  Leaving them with a
  well-formed document that is subtly changed from its state before
  the error would be especially bad. Recovery means to preserving the
  effects of actions issued before the last one, so the document
  appears unchanged.

### What About Recovery From Bugs?

We've just seen examples of recovery from an input error and of a
failure.  What would it mean to recover from a bug? It's not entirely
clear.

First, the bug needs to be detected, and that is not assured. As we
saw in the previous chapter, not all precondition violations are
detectable. Also, it's important to admit that when a runtime bug
check fails, we're not detecting the bug per-se: since bugs are flaws
in *code*, truly detecting bugs involves analyzing the program.
Instead, a runtime check detects a *downstream effect* that the bug
has had on *data*. When we observe that a precondition has been
violated, we know something invalid occurred, but we don't necessarily
know exactly where, how, or the full extent of the damaged data.

So can we “sally forth unscathed?”  The problem is that we can't
know. Since we don't know where the bug is, the downstream effects of
the problem could have affected many things we didn't test for.
Because of the bug, your program state could be very, very scathed
indeed, violating assumptions made when coding and potentially
compromising security, If user data is quietly corrupted and
subsequently saved, the damage becomes permanent.

In any case, unless the program has no mutable state and no external
effects, the only principled response to bug detection is to terminate
the process. [^fault-tolerant]

[^fault-tolerant]: There do exist systems that recover from bugs in a
principled way by using redundancy: for example, functionality could
be written three different ways by separate teams, and run in separate
processes that “vote” on results. In any case, the loser needs to be
terminated to flush any corrupted program state.

As terrible as that outcome may be, it's better than the
alternative. Recovery code is almost never exercised or tested and
thus is likely wrong, and the consequences of a botched recovery
attempt can be worse than termination. To no advantage, most recovery
code obscures the rest of the code and adds bloat, which hurts
performance.  Continuing to run after a bug is detected also hurts our
ability to fix the bug.  When a bug is detected, before any further
state changes, you want to immediately capture as much information as
possible that could assist in diagnosis.  In development that
typically means dropping into a debugger, and in deployed code that
might mean producing a crash log or core dump.  If deployed code
continues to run, the bug is obscured and—even if automatically
reported—will likely be de-prioritized until it is less
fresh and thus harder to address.  Worse, it can result in *multiple*
symptoms that will be reported as separate higher-priority bugs whose
root cause could have been addressed once.

## How to Handle Bugs

When a bug is detected, the best strategy is to stop the program
before more damage is done to data and generate a crash report or
debuggable image that captures as much information as is available
about the state of the program so there's a chance of fixing it.

Many people have a hard time accepting the idea of voluntarily
terminating, but let's face it: bug detection isn't the only reason
the program might suddenly stop.  The program can crash from an
*un*detected bug in unsafe code… or a person can trip over the power
cord, or the operating system itself could detect an internal bug,
causing a “kernel panic” that restarts the hardware.  Software should
be designed so that sudden termination is not catastrophic for its
users.

In fact, it's often possible to make restarting the app a completely
seamless experience. On an iPhone or iPad, for example, to save
battery and keep foreground apps responsive, the operating system may
kill your process any time it's in the background, but the user can
still “switch back” to the app.  When the user switches back, every
app is supposed to complete the illusion by coming back up in the same
state it was killed in.  So non-catastrophic early termination is
something you *can and should* design into your system. [^techniques]
When you accept that sudden termination is part of *every* program's
reality, it is easier to accept it as a response to bug detection, and
to mitigate the effects.

[^techniques]: Techniques for ensuring that restarting is seamless,
such as saving incremental backup files, are well-known, but outside
the scope of this book.

### Checking For Bugs

While, as we've seen, not all bugs are detectable, detecting as many
as possible at runtime is still a powerful way to improve code, by
finding detecting the presence of coding errors close to their source
and creating an incentive to prioritize fixing them.

#### Precondition Checks

Swift supplies a function for checking that a precondition is upheld,
which can be used as follows:

```swift
precondition(n >= 0)
```

*or*

```swift
precondition(n >= 0, "n == \(n); it must be non-negative.")
```

In either case, if the condition is false, the program will be
terminated (or stop if run in a debugger). [^Onone] In debug builds,
the file and line of the call will be written to the standard error
stream, along with any message supplied.  In release builds, to save
on program size, nothing is printed and any expression passed as a
second argument is never evaluated.

[^Onone]: Actually, if you build your program with `-Onone`, both
    forms have no effect; the conditional expression will never even
    be evaluated.  However, `-Onone` makes Swift an unsafe language:
    any failure to satisfy preconditions can cause *arbitrary
    behavior*. The results can be so serious that we strongly advise
    against using `-Onone`, except as an experiment to satisfy
    yourself that Swift's built-in checks do not have unacceptable
    cost.  The rest of this book is therefore written as though
    `-Onone` does not exist.

#### Assertions

Swift supplies a similar function called `assert`, modeled on the one
from the C programming language.  Its intended use is as a “soundness
check,” to validate your own assumptions rather than to make checks at
function boundaries.  For example, in the binary search algorithm
mentioned in the previous chapter,

```swift
  // precondition: l <= h
  let m = (h - l) / 2
  h = l + m
  // postcondition: l <= h
```

There is no contract supplying the Hoare-style precondition and
postcondition you see there; they are internal to a single function.
If violated, they indicate we've failed to understand the code we've
written: the informal proof we used to evaluate the function's
correctness was flawed. Replacing those comments with assertions can
help us uncover those failures during testing of debug builds without
impacting performance of release builds:

```swift
  assert(l <= h)
  let m = (h - l) / 2
  h = l + m
  assert(l <= h, "unexpected h value \(h)")
```

Similarly, `assert` can be useful for ensuring loop invariants are
correct (see the algorithms chapter). When trying to track down a
mysterious bug, temporarily adding as many assertions as possible in
the problem area can be a useful technique for narrowing the scope of
code you have to review.

Assertions are checked only in debug builds, compiling to nothing in
release builds. This has the useful effect of allowing programmers to
use `assert`s liberally without concern for slowing down release
builds.

#### Postcondition and Expensive Precondition Checks

Checking postconditions is the role of unit tests, so in most cases we
recommend leaving postcondition checks out of function bodies.
However, if you can't be confident that unit tests cover enough cases,
since postconditions are often expensive to check, it might make sense
to use assertions to check them as a confidence-building
measure. Similarly, a precondition that can only be checked with a
significant cost to preformance could be checked with
`assert`. However, in both cases we suggest using a forwarding
function whose name describes its meaning, so that `assert` is
used directly only for internal soundness checks:

public func preconditionUncheckedInRelease(
  _ condition: @autoclosure () -> Bool,
  _ message: @autoclosure () -> String = "",
  file: StaticString = #file, line: UInt = #line
) {
  assert(
    condition() || (
      false, fatalError("Precondition violated: \(message())",
      file: file, line: line)).0)
}

public func postconditionUncheckedInRelease(
  _ condition: @autoclosure () -> Bool,
  _ message: @autoclosure () -> String = "",
  file: StaticString = #file, line: UInt = #line
) {
  assert(
    condition() || (
      false, fatalError("Postcondition violated: \(message())",
      file: file, line: line)).0)
}
```

The distinction between these checks and a use of `assert` is important:
on failure, these indicate a bug in the caller, while a failed
`assert` normally indicates a bug in the callee. [^tricky]

[^tricky]:

All that said, resist the temptation to turn off a precondition check
in release builds before measuring its effect on performance.  The
value of stopping the program before things go too far wrong is
usually higher than the cost of any particular check.  Certainly, any
precondition check in a safe function that ultimately prevents an
unsafe component from being misused can never be turned off in release
builds.

```swift
extension Array {
  /// Exchanges the first and last elements.
  mutating func swapFirstAndLast() {
    precondition(!self.isEmpty)
    if count() == 1 { return } // swapping would be a no-op.
    withUnsafeBufferPointer { b in
      f = b.baseAddress
      l = f + b.count - 1
      swap(&f.pointee, &l.pointee)
    }
  }
}
```

In this example, the precondition check prevents an out-of-bounds
access to a non-existent first element.

## Failures

As much as we all love bugs, it's time to leave them behind and talk
about failures.  Let's say you identify a condition where your
function is unable to fulfill its primary purpose.  That can occur one
of two ways:

1. Something your function uses has a precondition that you can't
   be sure would be satisfied:

   ```swift
   extension Array {
     /// Returns the number of unused elements when a maximal
     /// number of `n`-element chunks are stored in `self`.
     func excessWhenFilled(withChunksOfSize n: Int) {
       count() % n // n == 0 would violate the precondition of %
     }
   }
   ```

2. Something your function uses can itself report a failure:

   ```swift
   extension Array {
     /// Writes a textual representation of `self` to a temporary file
     /// whose location is returned.
     func writeToTempFile(withChunksOfSize n: Int) -> URL {
       let r = FileManager.defaultTemporaryDirectory
         .appendingPathComponent(UUID().uuidString)
       "\(self)".write( // compile error: call can throw; error not handled
           to: r, atomically: false, encoding: .utf8)
       return r
     }
   }
   ```

> Note: both of the examples above are incomplete.

In general, when a condition *C* is necessary for fulfilling your
postcondition, there are three possible choices: you can make *C* a
precondition of your function, you can have your function throw an
`Error`, or you can weaken the postcondition, usually by making the
function return an `Result<T, Error>` instead of a
`T`.[^failable-initializer]

[^failable-initializer]: Most functions that return `Optional<T>`, and
    what Swift calls a “failable initializer” (declared as `init?(…)`)
    can be thought of as taking a “weakened postcondition” approach.
    Despite the name “failable initializer,” by our definition an
    optional result represents not a failure, but a successful
    fulfillment of the weak postcondition. Producing an `Optional<T>`
    rather than a `Result<T, E>` is appropriate when there is no
    useful distinction among the reasons that the function can't
    produce a `T` (which includes the case that there is only one
    possible reason).

A precondition is appropriate when:

- It is **possible for the caller to ensure** *C* is fulfilled.  In the
  second example above, the call to `write` can fail because the
  storage is full. Even if the caller were to measure free space
  before the call and find it sufficient, other processes could fill
  that space before the call to `write`. We must report a failure in
  this case:

   ```swift
   extension Array {
     /// Writes a textual representation of `self` to a temporary file
     /// whose location is returned.
     func writeToTempFile(withChunksOfSize n: Int) throws -> URL {
       let r = FileManager.defaultTemporaryDirectory
         .appendingPathComponent(UUID().uuidString)
       try "\(self)".write(to: r, atomically: false, encoding: .utf8)
       return r
     }
   }
   ```

- The work required for the caller to ensure the precondition is much
  cheaper than the call it is making.  For example, when deserializing
  a document you might discover that the input is corrupted. The work
  required by a caller to check for corruption before the call is
  usually nearly as high as the cost of deserialization, so
  well-formedness would be an inappropriate precondition for
  deserialization.  That said, remember that ensuring a precondition
  can often be done *by construction*, which makes it free. If this
  input is always known to be machine-generated by the same program
  that parses it, a precondition is an appropriate choice.

When both of these conditions are satisfied, you should prefer the
precondition, because, in general:

- Making *C* a precondition classifies ¬*C* as a bug in the caller,
  which aids reasoning about the source of misbehaviors. When all
  inputs are allowed, an opportunity to easily identify the incorrect
  code is lost.
- Even if you had chosen one of the other options, most clients will
  have satisfied *C* by construction at the point of the call.
- Making a client deal with the possibility of a reported error or
  return values that will never occur forces them to think about the
  case and write code to deal with it.
- Adding error reporting or expanded return values to a function
  inevitably generates code and some performance. Most often these
  results can't be handled in the immediate caller, so are propagated
  upwards, meaning these costs tend to spread to callers, and their
  callers, and so forth.  This applies even in Swift where the control
  flow implied by `try` is implicit.
- The viral nature adds complexity to function signatures, either
  by `throws` annotations or by more complex types such as `Result`.

### The Non-Precondition Approaches

Throwing is a syntactic optimization for the case where the immediate
caller will propagate the error to *its* caller, which can be done
with a simple `try` label on the expression containing the call.
Doing anything else with the error in the caller requires a much
heavier `do { ... } catch ... { ... }` construct.  Because errors are
propagated much more often than they are handled Swift has a
first-class language feature—`throw`—to express that pattern.


###
- therefore Dynamic type

Whether
to `throw` or weaken the postcondition is a judgement call


When a precondition is not viable, the choice whether to weaken the
postcondition or throw an `Error` is a judgement call.

### Failures Are Not A Part of Postconditions

The fact that failures report an inability to satisfy postconditions
means that their details—and the possibilty that they occur—means that
unlike return values, they **are not documented in the description of
the postcondition**. If you find this difference counterintuitive,
consider our rationale

The fact that the vast majority of errors are not handled in the
immediate caller, but instead propagated up the call chain, is
consequential.

and in many cases
may not be described at all except at a module level, e.g.

> Any `ThisModule` function that `throws` may report a
> `ThisModule.Error`.


## It's just API design to tell people about the errors you think they can handle.

Since a type satisfying a protocol with functions marked `throws` may
throw arbitrary errors, a module with generic components would often
have to add

> or any errors reported by types satisfying protocol requirements of
> the function.

This wrinkle means there is not much value to being more precise than

> Any `ThisModule` function that `throws` may report arbitrary errors,
> including `ThisModule.Error`.


So why am I tying this definition to postconditions other than to bind our understanding of error handling to our understanding of correctness?

First of all, it simplifies and improves understandability of contracts.  This is easiest to see if you have a dedicated language mechanism for error handling:

** Note: fictional programming language **

// Returns `x` sorted in `order`, or throws an exception
// in case order fails.
fn sorted(x: [Int], order: Ordering<Int>) throws -> [Int]

// Returns `x` sorted in `order`.
fn sorted(x: [Int], order: Ordering<Int>) throws -> [Int]

Even if you feel you need to say something about possible failures, that becomes a secondary note that's not essential to the contract.

// Returns `x` sorted in `order`.
//
// Propagates any exceptions thrown by `order`.
fn sorted(x: [Int], order: Ordering<Int>) throws -> [Int]

A programmer can know everything essential from the summary fragment and the signature.  Another way this separation plays nicely with exceptions is that you can say the postcondition of a function describes what you get when it returns, and a throwing function never returns.

If you don't use exceptions, you still simplified contracts as long as you have dedicated types to represent the possibility of failure.

// Returns `x` sorted in `order`.
fn sorted(x: [Int], order: Ordering<Int>) -> ResultOrFailure<[Int]>

Separating the function's primary intention from the reasons for failure makes sense, because the reasons for failure matter less.  If that's not obvious yet, some justification is coming.

Another reason to exclude the failure case from the postcondition is that you want postconditions to be solid and fully described, but a mutating operation that fails often leaves behind a state that's very difficult to nail down, and as I said in the contracts talk, that you usually don't want to nail down, because it's detail nobody cares about.  But if it's part of the postcondition, you need to say something about it, and that further complicates the contract.

// Sorts `x` according to `order` or throws an exception
// if `order` fails, leaving `x` modified in unspecified
// ways.
fn sort(mutating x: [Int], order: Ordering<Int>) throws

// Sorts `x` according to `order`.
fn sort(mutating x: [Int], order: Ordering<Int>) throws

### Two kinds of failures

If you've spent some time writing code that carefully handles failures, especially in a language like C where all the error propagation is explicit, failures start to fall into two main categories: local and non-local, based on where the recovery is likely to happen.

Local recovery occurs very close to the source of failure, usually in the immediate caller, in a way that often depends heavily on the reasons for the failure.  In many cases, the recovery path is performance-critical.

**Example**: you have an ultrafast memory allocator that draws from a local pool much smaller than your system memory.  You build a general-purpose allocator that first tries your fast allocator, and only if that allocation fails, recovers by trying the system allocator.

**Example**: the lowest level function that tries to send a network packet can fail for a whole slew of reasons (https://www.ibm.com/docs/en/zos/2.3.0?topic=codes-sockets-return-errnos), some of which may indicate a temporary condition like packet collision.  99% of the time, the immediate caller is a higher-level function that checks for these conditions and if found, initiates a retry protocol with exponential backoff, only itself failing after N failed retries.  That lowest-level failure is local.  The failure after N retries is very likely to be non-local.

Non-local recovery, which is far more common, occurs far from the source, usually in a way that can be described without reference to the reasons for failure.  For example,  when you're serializing a complex document,  serializing any part means serializing all of its sub-parts, and parts are ultimately nested many layers deep. Because you can run out of space in the serialization medium, every step of the process can fail.  If you write out the error propagation explicitly, it usually looks like this:

// Writes `s` into the archive.
fn serialize_section(s: Section) -> MaybeFailure<ArchiveFull,IOError,Unknown>
{
  var failure: Optional<FailureCode> = none;

  failure = serialize_part1(s.part1);
  if failure != none { return failure; }

  failure = serialize_part2(s.part2);
  if failure != none { return failure; }

  ...

  return serialize_partN(s.partN);
}

After every operation that can fail, you're adding “and if there was a failure, return it.”

There are many layers of this propagation.  None of it depends on the details of the reasons for failure: whether the disk is full or the OS detects directory corruption, or serialization is going to an in-memory archive and you run out of memory, you're going to do the same thing.  Finally, where propagation stops and the failure is handled—let's say this is a desktop app— again, the recovery is usually the same no matter the reasons for the failure: you report the problem to the user and wait for the next command.

#### Interlude: Exceptions?

Way back in 1996 I embarked on a mission to dispel the widespread fear, loathing, and misunderstanding around exceptions.  Yes I'm old.  While I've seen some real progress on that over the years, I know some of you out there are still not all that comfortable with the idea. If you'll let me, I think I can help.

##### Just control flow

Cases like this are where the motivation for exceptions becomes really obvious. They eliminate the boilerplate and let you see the code's primary intent:

// Writes `s` into the archive.
fn serialize_section(s: Section) throws {
  serialize_part1(s.part1);
  serialize_part2(s.part2);
  ...
  serialize_partN(s.partN);
}

There's no magic.  Exceptions are just control flow.  Like a switch statement, they capture a commonly needed pattern control flow pattern and eliminate unneeded syntax.

To grok the meaning of this code in its full detail, you mentally add “and if there was a failure, return it” everywhere.  But if you push failures out of your mind for a moment you can see that how the function fulfills its primary purpose leaps out at you in a way that was obscured by all the failure handling.  The effect is even stronger when there's some control flow that isn't related to error handling.

##### Also, type erasure

OK, I lied a little when I said exceptions are just control flow.  There's one other big difference between the exception version and the explicit version: the exception version erases the types of the failure data, and catch blocks are just big type switches with dynamic downcasts.

Lots of us are “static typing partisans,” so at first this might sound like a bad thing, but remember, as I said, none of the code propagating this failure (or even recovering from it usually) cares about its details.  What do you gain by threading all this failure information through your code?  When the reasons for failure change you end up creating a lot of churn in your codebase updating those types.

In fact, if you look carefully at the explicit signature, you'll see something that typically shows up when failure type information is included: people find a way to bypass that development friction.

fn serialize_section(s: Section) -> MaybeFailure<ArchiveFull,IOError,Unknown>

Here an “unknown” case was added that is basically a box for any failure type.  This is also a reason that systems with statically checked exception types are a bad idea.  Java's “checked exceptions” are a famously failed design because of this dynamic.

Swift recently added statically-typed error handling in spite of this lesson that should be well-understood to language designers, for reasons I don't understand.  There was great fanfare from the community, because, I suppose, everybody thinks they want more static type safety. I'm not optimistic that this time it's going to work out any better.

The moral of the story: sometimes dynamic polymorphism is the right answer.  Non-local error handling is a key example, and the design of most exception systems optimize for that.

#### When (and when not) to use exceptions

There's a lot of nice sounding advice out there about this that is either meaningless or vague, like “use exceptions for exceptional conditions,” or “don't use exceptions for control flow.”  I know that one is really popular around Adobe, but c'mon: if you're using exceptions, you're using them for control flow.  I hope to improve on that advice a little bit.

First of all, you can use exceptions for things that aren't obviously failures, like when the user cancels a command.  An exception is appropriate because the control flow pattern is identical to the one where the command runs out of disk space: the condition is propagated up to the top level.  In this case recovery is slightly different: there's nothing to report to the user when they cancel, but all the intermediate levels are the same.  It would be silly to explicitly propagate cancellation in parallel with the implicit propagation of failures.

But if you make this choice, I strongly urge you to classify this not-obviously-a-failure thing as a failure!  Otherwise you'll undo all the benefits of separating failures from postconditions, and you'll have to include “unless the user cancels, in which case…” in the summary of all your functions.  So in the end, my broad advice is, “only use exceptions for failures (but be open minded about what you call a failure).”  Actually, even if you're not using exceptions, any condition whose control flow follows the same path as non-local failures should probably be classified as a failure.

Another prime example is the discovery of a syntax error in some input.  In the general case, you are parsing this input out of a file. I/O failures can occur, and will follow the same control flow path.  Classifying your syntax error as a failure and using the same reporting mechanism is a win in that case.

Next, don't use exceptions for bugs. As we've said, when a bug is detected the program cannot proceed reliably, and throwing is likely to destroy valuable debugging information you need to find the bug, leave a corrupt state, open a security hole, and hide the bug from developers.  Even though the “default behavior” of exceptions is to stop the program, throwing defers the choice about whether to actually stop to every function above you in the call stack.  This is not a service, it's a burden. You've made your function harder to use by giving your clients more decisions to make.  Just don't.

That also means if you use components that misguidedly throw logic_errors, domain_error, invalid_argument, length_error or out_of_range at you, you should almost always stop them and turn them into assertion failures.  All that said, there are some systems, like Python, where using exceptions for bugs (to say nothing of exiting loops!) is so deeply ingrained that it's unavoidable. In python you have to ignore this rule.

Don't use exceptions for local failures.  As we've seen, exceptions are optimized for the patterns of non-local failures.  Using them for local failures means more catch blocks, which increase code complexity.  It's usually easy to tell what kind of failure you've got, but if you're writing a function and you really can't guess whether its failure is going to be handled locally, maybe you should write two functions.

Next, consider performance implications.  Most languages aren't like this, but most C++ implementations are usually biased so heavily toward optimizing the non-failure cases that handling a failure runs one or two orders of magnitude slower.  Usually that's a great trade-off because it allows them to skip checking for the error case on the hot path, and non-local failures are rare and don't happen repeatedly inside tight loops. But if you're writing a real-time system for example, you might want to think twice.

Here's an example that might open your mind a bit: when we were discussing the design of the Boost C++ Graph Library, we realized that occasionally a particular use of a graph algorithm might want to stop early.  For example, Dijkstra's algorithm finds all the paths from A to B in order, from shortest to longest.  What if you want to find the ten shortest paths and stop?  The way this library's algorithms work, you pass them a “visitor” object that gets notified about results as they are discovered.  And in fact there are lots of notification points for intermediate conditions, not just “complete path found,” so if we were going to handle this early stop explicitly, we'd generate a test after each one of these points in the algorithm's inner loop.  Instead, we decided to take advantage of the C++ bias toward non-failures.  We said a visitor that wants to stop early can just throw.  Now in fairness, I don't think we ever benchmarked the effects of this choice, so it might have been wrong in the end.  But it was at least plausibly right.

Finally, you might need to consider your team's development culture and use of tooling.  If people typically have their debuggers set up to stop when an exception occurs, you might need to take extra care not to throw when there's an alternate path to success.  Some developers tend to get upset when code stops in a case that will eventually succeed.

### How to Handle Failure

OK, enough about exceptions.  Finally we come to the good part!  Seriously, this was originally going to be the focus of the entire talk.

Let's talk about the obligations of a failing function and of its caller.  What goes in the contract and what does each side need to do to ensure correctness?

#### Callee

Documentation:
Document local failures and what they mean.
Document non-local failures at their source, but not where they are simply propagated. That information can be nice to have, but it also complicates contracts and is a burden to propagate and keep up-to-date.

Code:
Release any unmanaged resources you've allocated (e.g. close temporary file).

##### Optional

If mutating, consider giving the strong/transactional guarantee that if there is a failure, the function has no effects.

Only do this if it has no performance cost. Sometimes it just falls out of the implementation.  Sometimes you can get it by reordering the operations.  For example, if you do all the things that can fail before you mutate anything visible to clients, you've got it.

Don't pay a performance penalty to get it because not all clients need it and when composing parts all the needless overheads add up massively.

#### Caller

- Discard any partially-completed mutations to program state or propagate the error and that responsibility to your caller.  This partially mutated state is meaningless.

What counts as state?  Data that can have an observable effect on the future behavior of your code.  Your log file doesn't count.

##### Implications as data structures scale up

The only strategy that really scales in practice, when mutation can fail, is to propagate responsibility for discarding partial mutations all the way to the top of the application.  That in turn implies mutating a copy of existing data and replacing the old copy only when mutation succeeds.  Either way, you probably end up with a persistent data structure (which is a confusing name—it has nothing to do with persistence in the usual sense).

A persistent data structure is one where a partial mutation of a copy shares a lot of storage with the original.  For example, in Photoshop, we store a separate document for each state in the undo history, but these copies share storage for any parts that weren't mutated between revisions.  This sharing behavior falls out naturally when you compose your data structure from copy-on-write parts.

#### What (not) to do when an assertion fires.

- Don't remove the assertion because “without that the program works!”
- Don't complain to the owner of the assertion that they are crashing the program.
- Understand what kind of check is being performed
 - If it's a precondition check, fix your bug
 - If it's a self-check or postcondition check, talk to the code owner about why their assumptions might have been violated

#### Probably different functions for unit testing.








Notes:
  - read from network, how much was read
    - no-error case exists
    - podcast
    - likely a local handling case.
    - don't go to vegas with something you're not prepared to lose.

Quickdraw GX: 15% performance penalty for making silent null checks.

David Sankel   50:11
Folks can go ahead and put your hands up if you would like to.
Uh.
Ask a question.
Build a queue.

Dave Abrahams   50:22
I have the feeling that I didn't.
I didn't quite adequately deal with everybody's.
I questions that came up during the talk, so I'm happy to revisit those.
Got one hand?

David Sankel   50:36
At Philip, go ahead.

Philip Levy   50:38
And like to go back to a comment you made about.
The Boost graph library and raising exceptions to terminate that and you were pondering whether that was actually a good thing to have done based on performance, and it was wondering, is the notion that the fact that a visitor could raise an exception affecting performance of the execution you know of of non exceptional cases or just the cost of terminating the the algorithm by just raising that one exception?

Dave Abrahams   51:21
OK, I'm I'm going to try to try to answer your question as I understand, but I'm OK.

Philip Levy   51:28
Well, let me just clarify a little bit.
My expectations would be that raising an exception to terminate the algorithm wouldn't affect the performance of the execution of the algorithm.
The termination is a one time thing versus you know many thousands of nodes.
You may be looking at and so I was wondering why you were pondering that.

Dave Abrahams   51:47
Right.
That's the trade off we thought would love me.
So.
So Philip, yes, that that's the tradeoff that we thought we were making we because because C++ biases in favor of the straight line code, we thought this would be, this would be a good optimization.
My my reason for questioning it is I don't think we ever actually did any measurements.
That's all.

Philip Levy   52:16
OK, alright.
So it's it's an unknown, but there's no reason to believe it would be a problem.

Dave Abrahams   52:22
Right, that's correct.

Philip Levy   52:24
OK. Thank.
Thank you.

Dave Abrahams   52:27
I suppose if these graph algorithms were themselves used in tight loops on small problems where where the amount of straight line execution was low and you were throwing exceptions to terminate, that would be that would be bad, right?
If the algorithm was used repeatedly, umm, go ahead.

Sean Parent   52:48
So I think the others, I, David, there is there was an assumption that the checks at each node to see if there was a termination requested would be expensive and under modern hardware it probably costs you something, but it's a little hard to say.

Dave Abrahams   53:13
Yeah, I mean, you know, it's really hard to say without measuring.

Sean Parent   53:14
She tested.

Dave Abrahams   53:17
That's pretty much always the case for for performance.
You know, there's a there's a solid argument that, you know, the the functions on visitors are usually inlined.
When all of those intermediate visit points are are, you know are no OPS, the compiler can see it, and then it could skip the checks.
So like you know, the lesson is always measured before you make conclusions about performance.
