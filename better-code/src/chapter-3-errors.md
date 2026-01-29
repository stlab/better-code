# Errors

In the *Contracts* chapter you may have noticed we made this reference
to the concept of *errors*:

> If the preconditions are met, but the postconditions are not, and
> the function does not report an error, we'd say the method has a
> bug.

In the interest of progressive disclosure, we didn't look closely at
the idea, because behind that simple word lies a chapter's worth of
discussion.  Welcome to the *Errors* chapter!

What we present here is not the only logically consistent approach to
errors, and our approach may clash with your instincts.  It is the
result of optimizing for local reasoning and the ergonomics of
scalable software development, and the justifications for our choices
are interdependent.  We hope you'll bear with us as we tie them all
together.

## Definitions

To understand any topic, it's important to define it crisply, and
unfortunately “error” and associated words have been used rather
loosely, and previous attempts to define these words have relied on
other words, like “expected,” which themselves lack clear definitions,
at least when it comes to programming.

Unless we want to invent new terms, we will have to impose a little of
our own structure on the usual terminology. We hope these definitions
are at least consistent with your understanding:

> **Error**: anything that prevents a function from fulfilling its
> postcondition.

When we write the word “error” in normal type, we mean the idea above,
distinct from the related Swift `Error` protocol, which we'll always
spell in code font.

Errors come in two flavors:[^common-definition]

> - **Programming Error**, or **bug**: code contains an
>    avoidable[^avoidable] mistake. For example, an `if` statement
>    tests the logical inverse of the correct condition.
>
> - **Runtime error**: a function could not fulfill its postconditions
>   even though its preconditions were satisfied.  For example,
>   writing a file might fail because the filesystem is full.

[^avoidable]: While bugs in general are inevitable, every *specific*
    bug is avoidable.

[^common-definition]: While some folks like to use the word “error” to
refer only to what we call *runtime errors*—as the authors have done
in the past—the use of “error” to encompass both categories seems to
be the most widespread practice. We've adopted that usage to avoid
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
identifier rather than a misspelled keyword, and issues five unhelpful
errors, four of which point to the remaining otherwise-valid code.
That's not an indictment of Swift; doing this job correctly is
nontrivial.

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
newly-incorrect assumptions.  Second, it means that the state makes
sense given the correct inputs received so far. “Making sense” is a
subjective judgement. For example:

- The initial state of a compiler, before it has seen any input, meets
  the compiler's invariants. But when a syntax error is encountered,
  resuming from its initial state would discard the context seen so
  far. Unless the input following the error would have been legal at
  the beginning a source file, the compiler will issue many unhelpful
  diagnostics for that following input. Recovery means accounting
  somehow for the non-erroneous input seen so far and re-synchronizing
  the compiler with what follows.

- In a desktop graphics application, it's not enough that upon error
  (say, file creation fails), the user has a well-formed document; an
  empty document is not an acceptable result.  Leaving them with a
  well-formed document that is subtly changed from its state before
  the error would be especially bad. “Recovery” in this case means
  preserving the effects of actions issued before the last one, so the
  document appears unchanged.

### What About Recovery From Bugs?

We've just seen examples of recovery from two kinds of runtime error.
What would it mean to recover from a bug? It's not entirely clear.

First, the bug needs to be detected, and that is not assured. As we
saw in the previous chapter, not all precondition violations are
detectable. Also, it's important to admit that when a precondition
check fails, we're not detecting the bug per-se: since bugs are flaws
in *code*, truly detecting bugs involves analyzing the program.
Instead, a runtime check detects a *downstream effect* that the bug
has had on *data*. When we observe that a precondition has been
violated, we know there is invalid code, but we don't know exactly
where it is, nor can we be sure of the full extent of damaged data.

So can we “sally forth unscathed?”  The problem is that we can't
know. Since we don't know where the bug is, the downstream effects of
the problem could have affected many things we didn't test for.
Because of the bug, your program state could be very, very scathed
indeed, violating assumptions made when coding and potentially
compromising security. If user data is quietly corrupted and
subsequently saved, the damage becomes permanent.

In any case, unless the program has no mutable state and no external
effects, the only principled response to bug detection is to terminate
the process. [^fault-tolerant]

[^fault-tolerant]: There do exist systems that recover from bugs in a
principled way by using redundancy: for example, functionality could
be written three different ways by separate teams, and run in separate
processes that “vote” on results. In any case, the loser needs to be
terminated to flush any corrupted program state.

As terrible as sudden termination may be, it's better than the
alternative. Attempting to recover means adding code, and recovery
code is almost never exercised or tested and thus is likely wrong, and
the consequences of a botched recovery attempt can be worse than
termination. To no advantage, most recovery code obscures the rest of
the code and adds needless tests, which hurts performance.  Continuing
to run after a bug is detected also hurts our ability to fix the bug.
When a bug is detected, before any further state changes, we want to
immediately capture as much information as possible that could assist
in diagnosis.  In development that typically means dropping into a
debugger, and in deployed code that might mean producing a crash log
or core dump.  If deployed code continues to run, the bug is obscured
and—even if automatically reported—will likely be de-prioritized until
it is less fresh and thus harder to address.  Worse, it can result in
*multiple* symptoms that will be reported as separate higher-priority
bugs whose root cause could have been addressed once.

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
still “switch back” to the app.  At that point, every
app is supposed to complete the illusion by coming back up in the same
state in which it was killed.  So non-catastrophic early termination is
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
    any failure to satisfy preconditions can cause *undefined
    behavior*. The results can be so serious that we strongly advise
    against using `-Onone`, except as an experiment to satisfy
    yourself that Swift's built-in checks do not have unacceptable
    cost.  The rest of this book is therefore written as though
    `-Onone` does not exist.

#### Assertions

Swift supplies a similar function called `assert`, modeled on the one
from the C programming language.  Its intended use is as a “soundness
check,” to validate your own assumptions rather than to make contract
checks at function boundaries.  For example, in the binary search
algorithm mentioned in the previous chapter,

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
help us uncover those flaws during testing of debug builds without
impacting performance of release builds:

```swift
  assert(l <= h)
  let m = (h - l) / 2
  h = l + m
  assert(l <= h, "unexpected h value \(h)")
```

Similarly, `assert` can be useful for ensuring loop invariants are
correct (see the algorithms chapter). When trying to track down a
mysterious bug, adding as many assertions as possible in the problem
area can be a useful technique for narrowing the scope of code you
have to review.

Assertions are checked only in debug builds, compiling to nothing in
release builds, thereby encouraging liberal use of `assert` without
concern for slowing down release builds.

### Postcondition and Expensive Precondition Checks

Checking postconditions is the role of unit tests and can be
compute-intensive, so in most cases we recommend leaving postcondition
checks out of function bodies.  However, if you can't be confident
that unit tests cover enough cases, using `assert` for some
postcondition checks in function bodies ensures there is no cost in
release builds.

Similarly, a precondition that can only be checked with a significant
cost to preformance could be checked with `assert`. Because—unlike
most uses of `assert`—a precondition failure indicates a bug in the
caller, it's important to distinguish these uses in the assertion
message:

```
assert(x.isSorted(), "Precondition failed: x is not sorted.")
```

That said, resist the temptation to skip a precondition check in
release builds before measuring its effect on performance.  The value
of stopping the program before things go too far wrong is usually
higher than the cost of any particular check.  Certainly, any
precondition check that prevents a safe function from misusing unsafe
operations must never be turned off in release builds.

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

The precondition check above prevents an out-of-bounds access to a
non-existent first element, and cannot be skipped without also making
the function unsafe (in which case “unsafe” should appear in the
function name).

## What To Do When Postconditions Can't Be Upheld

Suppose you identify a condition where your function is unable to
fulfill its postconditions, even though its preconditions are
satisfied.  That can occur one of two ways. (These examples represent
code in an unfinished state):

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

2. Something your function uses can itself report a runtime error:

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

In general, when a condition *C* is necessary for fulfilling your
postcondition, there are three possible choices:

1. You can make *C* a precondition of your function
2. You can make the function report a runtime error to its caller
3. You can weaken the postcondition (e.g. by returning
   `Optional<T>` instead of `T`). [^failable-initializer]


[^failable-initializer]: Most functions that return `Optional<T>`, and
    what Swift calls a “failable initializer” (declared as `init?(…)`)
    can be thought of as taking a “weakened postcondition” approach.
    Despite the name “failable initializer,” by our definition a `nil`
    result represents not a runtime error, but a successful fulfillment of
    the weakened postcondition.

### Adding a Precondition

It's appropriate to add a precondition when:

- It is **possible for the caller to ensure** *C* is fulfilled.  In
  the second example above, the call to `write` can fail because the
  storage is full (among other reasons). Even if the caller were to
  measure free space before the call and find it sufficient, other
  processes could fill that space before the call to `write`. We
  *cannot* make sufficient disk space a precondition in this case, so
  we should instead propagate the error:

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

- It is **affordable for the caller to ensure** the precondition.  For
  example, when deserializing a data structure you might discover that
  the input is corrupted. The work required by a caller to check for
  corruption before the call is usually nearly as high as the cost of
  deserialization, so validity is an inappropriate precondition for
  deserialization.  That said, remember that ensuring a precondition
  can often be done *by construction*, which makes it free. If the
  input is always known to be machine-generated by the same OS process
  that parses it, a precondition is an appropriate choice.

### Reporting a Runtime Error

Swift provides two ways to report runtime errors: `throw`ing an
`Error` and returning a `Result<T, E: Error>`. The choice of which to
use is an API design judgement call, but it is dominated by one
consequential fact:

> *In most cases*, when a callee can't fulfill its postconditions,
> neither can the caller—that inability instead propagates up the call
> chain to some general handler that restores the program to a state
> appropriate for continuing, usually after some form of error
> reporting.

Because this pattern is so common, most languages provide first-class
features to accomodate it without causing this kind of repeated
boilerplate:

    ```swift
    let someValueOrError = thing1ThatCanFail()
    guard case .success(let someValue) = someValueOrError else {
      return someValueOrError
    }

    let otherValueOrError = thing2ThatCanFail()
    guard case .success(let otherValue) = otherValueOrError else {
      return otherValueOrError
    }
    ```


Swift's thrown errors fill that role by propagating errors upward with
a simple `try` label on an expression containing the call.

    ```swift
    let someValue = try thing1ThatCanFail()
    let otherValue = try thing2ThatCanFail()
    ```

Doing anything with the error *other* than propagating it requires a
much heavier `do { ... } catch ... { ... }` construct, which is
slighly heavier-weight than the boilerplate pattern, making throwing a
worse choice when clients do not directly propagate errors.

The great ergonomic advantage of throwing in the common case means
that returning a `Result` only makes sense when it's very likely that
your callers will be able to satisfy their postconditions, *even when
faced with your runtime error*. For example, a low-level
function that makes a single attempt to send a network packet is very
likely to be called by a higher-level function that retries several
times with an exponentially-increasing delay before failing.  The
low-level function might return a `Result`, while the higher-level
function would throw. These cases, however, are *extremely* rare, and
if you have no special insight into your function's callers, choosing
to `throw` is a pretty good bet.[^uniform-choice]

[^uniform-choice]: Returning a `Result` could also make sense when
    most callers are going to transform the error somehow before
    propagating it, but code that propagates transformed errors is
    also very rare. The use cases for `Result` are rare enough, in
    fact, that it's a reasonable choice to always `throw` for runtime
    error reporting.


#### Dynamic Typing of Errors

The overwhelming commonality of propagation means that functions in
the call chain above the one initiating the error report seldom
depends on detailed information about thrown errors.  The usual
untyped `throws` specification in a function signature tells most
callers everything they need to use the function correctly.  In fact,
since reporting the error to a human is typically the only useful
response when propagation stops, the same often applies to the
function that ultimately catches the error: `any Error` provides
[`localizedDescription`](https://developer.apple.com/documentation/swift/error/localizeddescription)
for that purpose.

Swift does have a [“typed throws”
feature](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling#Specifying-the-Error-Type)
that lets you encode possible error types in the types of functions,
but we suggest you avoid it, because it doesn't scale well and tends
to “leak” what should be an implementation detail into a function's
interface.  Because failing in a new way can be a breaking change for
clients that use the same feature, it adds development friction
which—if overcome—causes ripples of change throughout a codebase.  In
languages with statically constrained error reporting, programmers
routinely circumvent the mechanism because it is a poor match for
common usage and has too high a cost to the development process.

You can think of a thrown error the same way you'd think of a returned
`any P` (where `P` is a protocol—`Error` in this case): we normally
don't feel obliged to specify all the possible concrete types that can
inhabit a given protocol instance, because the protocol itself
provides the interface clients are expected to use.  Just as an `is`
test or `as?` cast is *able* to interrogate the concrete type of a
protocol instance, so can a `catch` clause, but that ability does not
oblige a function to expose the details of those types.

Of course, an alternative to the “open” polymorphism of `any P` is the
“closed” polymorphism of an `enum`.  Each has its place, but for all
the reasons outlined above, open polymorphism is generally a better
fit for the use case of error reporting.

The exception to this reasoning is once again the case where clients
are very unlikely to directly propagate the error, in which case you
are likely to use `Result<T, E>` rather than throwing, and using a
more specific error type than `any Error` might make sense.

#### How to Document Runtime Errors

Because a runtime error report indicates a failure to fulfill
postconditions, information about errors—including that they are
possible—does not belong in a function's postcondition documentation,
whose primary home is the summary sentence fragment.[^result-doc]

[^result-doc]: This rule creates a slightly awkward special case for
    functions that return a `Result<T,E>`, which should be documented
    as though they just return a `T`:

    ```swift
    extension Array {
      /// Writes a textual representation of `self` to a temporary file,
      /// returning its location.
      func writeToTempFile(withChunksOfSize n: Int)
        -> Result<URL,IOError>
      { ... }
    }
    ```

In fact, because most callers propagate errors, it's very common that
nothing about errors needs to be documented at all: `throws` in the
function signature indicates that arbitrary errors can be thrown and
no further information about errors is required to use the function
correctly.

That does not mean that possible error types and conditions should
*never* be documented.  If you anticipate that clients of a function
will use the details of some runtime error programmatically, it may
make sense to put details in the function's documentation. That said,
resist the urge to document these details just because they “might be
needed.” As with any other detail of an API, documenting errors that
are irrelevant to most code creates a usability tax that is paid by
everyone.  In any case, keeping runtime error information out of
postconditions (and thus summary documentation) works to simplify
contracts and make functions easier to use.

A useful middle ground is to describe reported errors at the module
level, e.g.

> Any `ThisModule` function that `throws` may report a
> `ThisModule.Error`.

A description like the one above does not preclude reporting other
errors, such as those thrown by a dependency like `Foundation`, but
calls attention to the error type introduced by `ThisModule`.

##### Documenting Mutating Functions

When a runtime error occurs partway through a mutating operation, a a
partially mutated state may be left behind. Trying to describe these
states in detail is usually a bad idea.  Apart from the fact that
such descriptions can be unmanageably complex—try to document the
state of an array from partway through an aborted sorting operation—it
is normally information no client can use.

Partially documenting these states *can* be useful, however.  For
example, [Swift's
`sort(by:)`](https://developer.apple.com/documentation/swift/array/sort(by:))
method guarantees that no elements are lost if an error occurs, which
can be useful in code that manages allocated resources, or that
depends for its safety on invariants being upheld (usually the
implementations of safe types with unsafe implementation details).
The following code uses that guarantee to ensure that all the
allocated buffers are eventually freed.

```swift
/// Processes each element of `xs` in an order determined by the
/// [total
/// preorder](https://en.wikipedia.org/wiki/Weak_ordering#Total_preorders)
/// `areInOrder` using a distinct 1Kb buffer for each one.
func f(_ xs: [X], orderedBy areInOrder: (X, X) throws -> Bool) rethrows
{
  var buffers = xs.map { x in
    (p, UnsafeMutablePointer<UInt8>.allocate(capacity: 1024)) }
  defer { for _, b in buffers { b.deallocate() } }

  buffers.sort { !areInOrder($1.0, $0.0) }
    ...
}
```

The **strong guarantee** that *no mutation occurs at all* in case
of an error is the easiest to document and most useful special case:

```swift
/// If `shouldSwap(x, y)`, swaps `x` and `y`.
///
/// If an error is thrown there are no effects.
func swap<T>(
  _ x: inout T, _ y: inout T, if shouldSwap: (T, T) throws->Bool
) rethrows {
  if try shouldSwap(x, y) {
    swap(&x, &y)
  }
}
```

A few caveats about mutation guarantees when errors occur:

1. Known use cases are few and rare: most allacated resources are
   ultimately managed by the `deinit` of some class, and uses of
   unsafe operations are usually encapsulated. Weigh the marginal
   utility of making guarantees against the complexity it adds to
   documentation.
2. Like any guarantee, they can limit your ability to change a
   function's implementation without breaking clients.
3. Avoid making guarantees if it has a performance cost.  For example,
   one way to get the strong guarantee is to order operations so the
   first mutation occurs only after all throwing operations are
   complete.  Some mutating operations can be arranged that way at
   little or no cost, but you can do it to *any* operation by copying
   the data, mutating the copy (which might fail), and finally
   replacing the data with the mutated copy.  The problem is that the
   copy can be expensive and you can't be sure all clients need it.
   Even when a client needs to give the same guarantee itself, your
   work may be wasted: when operations A and B give the strong
   guarantee, the operation C composed of A and then B does not (if B
   fails, the modifications of A remain). If you need a strong
   guarantee for C, another copy is required and the lower-level
   copies haven't helped at all.

### Weakening The Postcondition

There are several ways to weaken a postcondition. The first is to make
it conditional on some property of the function's inputs.  For
example, take the `sort` method from the previous chapter. Instead of
making it a precondition that the comparison is a total preorder, we
could weaken the postcondition as follows:

```swift
/// Sorts the elements so that all adjacent pairs satisfy
/// `areInOrder`, or permutes the elements in an unspecified way if
/// `areInOrder` is not a [total
/// preorder](https://en.wikipedia.org/wiki/Weak_ordering#Total_preorders)
/// `areInOrder`.
///
/// - Complexity: at most N log N comparisons, where N is the number
///   of elements.
mutating func sort(areInOrder: (Element, Element)->Bool) { ... }
```

As you can see, this change makes the API more complicated to no
advantage: an unspecified permutation is not a result any client wants
from `sort`.[^random-sort]

[^random-sort]: We've seen attempts to randomly shuffle elements using
    `x.sort { Bool.random() }`, but that has worse performance than a
    proper `x.randomShuffle()` would, and is not guaranteed to
    preserve the same randomness properties.  Perhaps more
    importantly, the code lies by claiming to sort when it in fact
    does not.

Another approach is to intentionally expand the range of values
returned.  For example, `Array`'s existing `subscript` could be
declared as:

```
/// The `i`th element.
subscript(i: Int) -> Element
```

but could have instead been designed this way:

```
/// The `i`th element, or `nil` if there is no such element.
subscript(i: Int) -> Element?
```

The change adds only a small amount of complexity to the contract, but
consider the impact on callers: every existing use of array indexing
now needs to be force-unwrapped.  Aside from the runtime cost of all
those tests and branches, seeing `!` in the code adds cognitive
overhead for human readers.  In the vast majority of callers, the
precondition of the original API is established by construction with
no special checks, but should a client need to check that an index is
in bounds, doing so is extremely cheap.

Occasionally, though, a weakened postcondition is appropriate.
Dictionary's `subscript` taking a key is one example:

```
/// The value associated with `k`, or `nil` if there is no such value.
subscript(k: Key) -> Value?
```

In this case, it's common that callers have not somehow ensured the
dictionary has a key `k`, and checking for the presence of the key in
the caller would have a substantial cost similar to that of the
subscript itself, so it's much more efficient to pay that cost once in
the `subscript` implementation.

### How to Choose?

Clearly weakening a postcondition seldom pays off and should be used
rarely.  Whenever it is appropriate, you should prefer to add a
precondition, because:

- It makes it easy to identify incorrect code. A failure to satisfy
  the condition becomes a bug in the caller, which aids in reasoning
  about the source of misbehaviors. If the precondition is checkable
  at runtime, you can even catch misuse in testing, *before* it
  becomes misbehavior.

- Making a client deal with the possibility of return values or
  runtime errors that will never occur in practice forces authors and
  readers of client code to think about the case and the code to
  handle it (or about why that code isn't needed).

- Adding error reporting or expanded return values to a function
  inevitably generates code and costs some performance. Most often
  these results can't be handled in the immediate caller, so are
  propagated upwards, spreading the cost to callers, their callers,
  and so forth.  (The control flow implied by `try` has a cost similar
  to the cost for checking and propagating a returned `Result<T, any
  Error>`).

- The alternatives complicate APIs.

Most of the time, when a precondition isn't added, it makes sense to
report a runtime error, because it preserves the idea of the
function's simple primary purpose, implying that all the other cases
are some kind of failure to achieve that purpose.  Weakening the
postcondition means considering more cases successful, which makes a
function into a multipurpose tool, which is usually harder to
document, use, and understand.

If you must weaken the postcondition, returning an `Optional<T>`
instead of a `T` adds the least possible amount of information to the
success case, and thus does the least harm to API simplicity. It can
be appropriate when there will never be a useful distinction among
reasons that the function can't produce a `T`. Subscripting a
`Dictionary` with its key type is a good example.  The only reason it
would not produce a value is if the key were not present.

Lastly, remember that the choice is in your hands, and what you choose
has a profound effect on clients of your code. There is no criterion
that tells us a condition must or must not be a runtime error other
than the effect it has on client code.

## Handling Runtime Errors Correctly

The previous section was about how to design APIs; this one covers how
to account for errors in function bodies.

### When Propagation Stops

Code that stops upward propagation of an error and continues to run
has one fundamental obligation: to discard any partially-mutated state
that can affect on the future behavior of your code (that excludes log
files, for example).  In general, this state is completely unspecified
and there's no other valid thing you can do with it.

For the same reasons that the strong guarantee does not compose,
neither does the discarding of partial mutations: if the second of two
composed operations fails, modifications made by the first
remain. So ultimately, that means responsibility for discarding partial
mutations tends to propagate all the way to the top of an application.

In most cases, the only acceptable behavior at that point is to
present an error report to the user and leave their data unchanged,
i.e. the program must provide the strong guarantee. That in turn
means—unless the data is all in a transactional database—a program
must usually follow the formula already given for the strong
guarantee: mutate a copy of the user's data and replace the data only
when mutation succeeds.[^persistent]

[^persistent]: This pattern is only reasonably efficient when the data
  is small or in a [persistent data
  structure](https://en.wikipedia.org/wiki/Persistent_data_structure).
  Because of Swift's use of
  [copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write) for
  variable-sized data, any data structure built out of standard
  collections can be viewed as persistent provided none are allowed to
  grow too large, but easier and more rigorous implementations of
  persistence can be found in
  [swift-collections](https://github.com/apple/swift-collections),
  e.g. [`TreeSet` and
  `TreeDictionary`](https://swiftpackageindex.com/apple/swift-collections/1.3.0/documentation/hashtreecollections)

### Mutating Functions

The fact that all partially-mutated state must be discarded has one
profound implication for invariants: in general, when an error occurs,
a mutating method need not restore any invariants it has broken.  It
can instead propagate the error to its caller with no further
ceremony!

The exception is the invariants of types whose safe operations are
implemented in terms of unsafe ones. Any invariants depended on to
satisfy preconditions of those unsafe operations must of course be
upheld to preserve the safety guarantees.

### Functions that Allocate Unmanaged Resources

Any resources such as open files or raw memory allocations that are
not otherwise managed must be released.  It's best to limit that
concern by making resource release the responsibility of some class'
`deinit` method.
