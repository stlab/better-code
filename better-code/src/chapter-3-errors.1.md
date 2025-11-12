# Better Code: Errors

So we're going to talk about errors and handling them.

So what's an error?

##  Words

When talking about anything, I like to start out by trying to define it, and reading existing definitions is usually a good way to start.  After all, programming is about communication, and if we want to communicate effectively we should use words in the expected ways.

Normally when I've done a version of this talk it's been a very interactive, in-person experience: I ask the audience for their definitions and we write them all on a board and then dissect them.  I don't think that's going to work in this context, so instead I asked the web.

That exercise was very revealing, and actually changed my mind about the meaning of error and the overall scope of the presentation.  So let's review what I found out.  These are roughly the top answers Google gave me when I asked it to define “error” and “error handling.”  Aside from Wikipedia, I was surprised at some of the hits it chose, but if you don't like them you can take it up with Google.  I feel pretty confident that these results reflect the way people talk about errors.

### Definitions

Wikipedia:

An error (from the Latin errāre, meaning 'to wander'[1]) is an inaccurate or incorrect action, thought, or judgement.[1]


In statistics, "error" refers to the difference between the value which has been computed and the correct value.[2] An error could result in failure or in a deviation from the intended performance or behavior.[3]

In human behavior the norms or expectations for behavior or its consequences can be derived from the intention of the actor or from the expectations of other individuals or from a social grouping or from social norms. (See deviance.) Gaffes and faux pas can be labels for certain instances of this kind of error. More serious departures from social norms carry labels such as misbehavior and labels from the legal system, such as misdemeanor and crime. Departures from norms connected to religion can have other labels, such as sin.

In science and engineering in general, an error is defined as a difference between the desired and actual performance or behavior of a system or object.

Engineers seek to design devices, machines and systems and in such a way as to mitigate or preferably avoid the effects of error, whether unintentional or not. Such errors in a system can be latent design errors that may go unnoticed for years, until the right set of circumstances arises that cause them to become active. Other errors in engineered systems can arise due to human error, which includes cognitive bias. Human factors engineering is often applied to designs in an attempt to minimize this type of error by making systems more forgiving or error-tolerant.



Error Message:

An error message is the information displayed when an unforeseen problem occurs, usually on a computer or other device. Modern operating systems with graphical user interfaces, often display error messages using dialog boxes. Error messages are used when user intervention is required, to indicate that a desired operation has failed, or to relay important warnings (such as warning a computer user that they are almost out of hard disk space).

Lenovo:

Computer error refers to a mistake or malfunction that occurs within a computer system, leading to unexpected or incorrect behavior.
Computer Hope:

An error describes any issue that arises unexpectedly that cause a computer to not function properly.

Vocabulary.com:Definitions of computer error
noun (computer science) the occurrence of an incorrect result produced by a computer
Toppr.com

An error in computer data is called Bug.

A software bug is an error, flaw, failure or fault in a computer program or system that causes it to produce an incorrect or unexpected result, or to behave in unintended ways.

https://textexpander.com/blog/most-common-programming-errors:
The 7 Most Common Types of Errors in Programming and How to Avoid Them
Syntax Errors
Logic Errors
Compilation Errors
Runtime Errors
Arithmetic Errors
Resource Errors
Interface Errors

Techopedia:

What Does Error Handling Mean?
Error handling refers to the response and recovery procedures from error conditions present in a software application. In other words, it is the process comprised of anticipation, detection and resolution of application errors, programming errors or communication errors. Error handling helps in maintaining the normal flow of program execution.

There are four main categories of errors:

Logical errors
Generated errors
Compile-time errors
Runtime errors

dremio.com:

Error Handling refers to the process of detecting, managing, and resolving errors and exceptions that occur during data processing and analytics. It involves implementing mechanisms and strategies to handle unexpected events and ensure data integrity and reliability.


OK, so in this text I want to highlight four things:

First, a lot of it, all this red stuff, is about bugs.  If you happened to read the abstract blurb that we used in the talk announcement, you know it said we'll clearly define “error” distinct from “bug,” but these results force me to admit that error usually means bug, and if I want to talk about non-bugs I might need to find a different term.  It also convinced me that in a talk about error handling you can't avoid the topic of how to deal with bugs. So we're going to talk about all kinds of errors, both bugs and the other kinds.

Since I love defining things, I'm going to take this opportunity to define “bug” as an avoidable coding error.

Statistically, bugs may be inevitable
but
Every individual bug is avoidable.

Which is a good thing, because you can't really plan for bugs; they could be anywhere.  That's why you see the word “unexpected” come up a lot in that red text.

Second, in a couple of places I colored green, people are talking about things that definitely aren't bugs, like resource allocation failure.  If I run out of space on the disk when I'm trying to save a document, that's not a bug.
Maybe it's rare, but you can predict that it will happen sometimes, and you know exactly where in your code it can happen, so you can plan a response for it. These non-bugs are what I used to call “errors” and had intended to be the sole topic of this talk. Let's call them failures.  They represent a failure—sometimes temporary—of the code to achieve its primary intent.

The blue highlight talks about errors due to cognitive bias, a very AI-forward concern.  Is that a bug?  I'm not sure cognitive bias is avoidable. So I guess I'd go with not-a-bug.  However, as far as I know it's not an event; it's a property of the code and/or dataset, so it's really in its own category.

Finally, these words in yellow talk about recovery, resolution, and maintaining data integrity.  How you achieve that is going to be important.

So there are three important parts to this picture:

Bugs
Failures (non-bugs, predictable obstacles)
Recovery and Integrity

## Recovery

So what do we mean by “recovery?” When I ask the web, most of the hits define error recovery in terms of what a parser does when it hits a syntax error in your code.

int main() {
  int x = 4
  //       ^---- error: expected ';' at end of declaration
  f(x);
  f(x x);
  //  ^--------- error: expected ')'
}

Let's say you left out a semicolon.  The parser could just stop there and issue one diagnostic about the missing symbol, if that's the only possibility in that syntactic position.  But most programming language parsers don't do that (even though I often wish they would).  They want to give me all the potentially-useful diagnostics about errors in the rest of my code.  If the parser just starts over, discarding its state and pretending the location of the error is the beginning of the file, I'm going to get lots of bogus error messages.  That's a pretty poor recovery because although the program continues, it's doing something that almost certainly doesn't make sense.

x.cpp:1:3: error: unknown type name 'f'
  f(x);
  ^
x.cpp:2:5: error: unknown type name 'x'
  f(x x);
    ^
x.cpp:2:3: error: a type specifier is required for all declarations
  f(x x);
  ^
x.cpp:4:1: error: extraneous closing brace ('}')
}
^


So instead parsers typically try to “recover” by pretending I had written something correct.  In this case it injects a phantom semicolon and continues.  So as a first cut, let's say recovery is continuing to execute, doing sensible work.  But I really like this quote from a stack overflow answer:

https://stackoverflow.com/a/38387506/125349

... i.e.:   "to sally forth, entirely unscathed, as though 'such an inconvenient event' never had occurred in the first place."

By “unscathed” they mean that the program state is intact: not only are the invariants upheld, but the state makes sense given the inputs the program has received.  If we have an error while applying a blur, it's not enough that the user's document is a well-formed file; it also can't have some random or half-finished changes they didn't ask for.

## Recovery from bugs?

OK, so let's talk about recovering from a bug.  What would that mean?
Well, first, it assumes you have some way to detect the bug; not all bugs are detectable, but let's assume this one is.  Typically that  means some precondition check fails: there's a bug in the caller that caused them to pass an invalid argument.

When that happens, you're not really detecting the bug, you're detecting one of its symptoms, like a cosmic echo.  The bug itself occurred at some indefinite point before that.  So can you ”sally forth unscathed?”  The problem is, you don't know.  Because of the bug, your program state could be very, very scathed indeed.

Sallying forth at this point is a terrible idea, for so many reasons.  First there are effects in the outside world:
- The user's data might be corrupted and they might save it that way, losing the last good state they had.
- The assumptions underlying any security evaluation you did may be violated, so you could be opening a security hole.
- You don't have enough information about the state of your system to do it reliably, you can't detect whether you've done it correctly, and the penalties we just discussed for failure to do it correctly are astronomical.


Continuing in the face of a known bug also has a terrible impact on the development process:
- The bug will be masked and will never get fixed…
- …until one day we're about to lose an important customer base because of that corruption.  And then you might spend weeks hunting the bug down because the customer sees a much more distant echo of the bug than the earlier echo your code detected.
- Most code is correct, so most of your bug-recovery code will never run.  It certainly won't be tested. All this recovery code bloats your program and every line is a liability with no offsetting benefits.

Some systems can recover from bugs (e.g. redundant ones).  Processes can't recover.

To sum up, in general you can't recover from bugs, and it's a bad idea to try.  So what can you do?

## Handling bugs

You can stop the program before any more damage is done, and generate a crash report or debuggable image that captures as much information as is available about the state of the program, so there's a chance of fixing the bug.  Maybe there's some small emergency shutdown procedure you need to perform, like saving information about the failing command so the application can offer to retry it for you when you restart it.

Let me be clear: THIS IS BAD. It could be experienced as a crash by users.
But it's the only way to prevent the much worse consequences of a botched recovery attempt.  Remember, the chances of botchery are high because you don't have enough information to do it reliably.
Upside: it will also be experienced as a crash by developers, QE teams, and beta testers, giving you a chance to fix the bug.

*** You can mitigate the experience of crashing ***
*** Don't tell me my assertion is a crash ***
*** An assertion is a controlled shutdown ***

A lot of people have a hard time accepting the idea of voluntarily terminating, but let's face it: your bug detection isn't the only reason the program might suddenly stop.  You can crash from an undetected bug.  Or a person can trip over the power cord.  You should design your software so that these bad things are not catastrophic.

*** In fact you could be more ambitious and try to make it really seamless.  You have to accept this is part of the UX package to even take this on. ***

In fact some platforms force you to live under a similar constraint.  On an iPhone or iPad, for example, to save battery and keep foreground apps responsive, the OS may kill your process any time it's in the background, but will make it look to the user like it's still running.  When the user switches back, every app is supposed to complete the illusion by coming back up in the same state it was killed in.  I can tell you as a user, it can be really jarring when you encounter an app that doesn't do it right.  The point is, resilience to early termination is something you can and should design into the system.

For example, Photoshop uses a variety of strategies: we always save documents into a new file and atomically swap it into place only after the save succeeds, so we never leave a half-saved document on disk.  We also periodically save backups so at most you only lose the last few minutes of work.  If we needed to tighten that up we could, by saving a record of changes since the last full backup.

## Assertions

The usual mechanism for terminating a program when a bug is detected is called an assertion and traditionally it spelled something like this:

	assert(n >= 0);

This spelling comes from C and C++.  If you're programming in another language, you probably have something similar.

The C assertion is pretty straightforward: either it's disabled, in which case it generates no code at all—even the check is skipped—or it does the check and exits immediately with a predefined error code if the check fails, usually printing a message containing the text of the failed check and its location in source.

Debuggers will commonly stop at the assertion rather than exiting, and even if you're not running in the debugger, on major desktop OSes, you'll get a crash report with the entire program state that can be loaded into a debugger.  So this is great for catching bugs early, before they get shipped, provided people use it.

Projects commonly disable assertions in release builds, which has the nice side-effect of making programmers comfortable adding lots of assertions, because they know they won't slow down the release build.  And more bugs get caught early.

But unless you really believe you're shipping bug-free software, you might want to leave most assertions on in release builds. In fact, the security of your software might depend on it.  If you're programming in an unsafe language like C++, opportunities to cause undefined behavior are all around you. When you can assert that the conditions for avoiding undefined behavior are met before executing the dangerous operation, the program will come to a controlled stop instead of opening an arbitrarily bad security hole.

The problem with leaving assertions on in release is that some checks are too expensive to ship. And let's be honest; many programmers will go with their gut, instead of measuring, when making that determination. We really need a second, expensive_assert(), that's only on in debug builds, so we continue to catch those bugs early.

There's another problem with having just one assertion: it doesn't express sufficient intent.  For example, it might be a precondition check, or the asserting function's author might just be double-checking their own reasoning.  When these two assertions fire, the meaning is very different: the first indicates a bug in the caller, the other one is a bug in the callee.  So I really want separate precondition and self_check functions.

If I'm writing in a safe-by-default language like Rust or Swift, the checks that prevent undefined behavior, like array bounds checks, are special: I can afford to turn off all the other checks in shipping code, but these checks are the ones upholding safety properties of my system are compromised.  So I want a different assertion for these checks, even if I don't ever anticipate turning off the other ones in a shipped product.  These are the ones that we can't delete from the code.  I might want to turn the other assertions off locally to measure how much overhead they are incurring.

I hope you get the idea.  I'm not going to prescribe the exact set of assertion facilities your project needs, but a carefully engineered suite of these functions with properties appropriate to your project is part of a comprehensive strategy for dealing with bugs.  If you haven't got one, go design it.

One last point about the C++ assert: it's better than nothing, but because it calls abort(), there's no place to put emergency shutdown measures.  You can't even display a message to the user, so to the user it will always feel like a hard, unceremonious crash.  You probably want failed assertions to call terminate() instead, because it allows terminate handlers can run.  So that's another reason to engineer your own assertions, even if you build just one.

## What if you're not allowed to terminate?

Fight for the right (to terminate). If the system is critical, advocate creating a recovery system outside the process.
If you lose today
Fail as noisily as possible, preferably by terminating in non-shipping code.
Keep fighting
Be prepared to win someday.  That means use a suite of assertions that don't terminate, but whose behavior you can change when you win the fight.

# Failures

OK, as much as we all love bugs, it's time to leave them behind and talk about failures.  Let's say you identify a condition X where your function is unable to fulfill its primary purpose.  That can occur one of two ways:


Something your function calls has a precondition that you're not sure would be satisfied.
Something your function calls can itself report a failure.

You usually have two choices at this point:
Make !X a precondition; X reflects a bug in the caller.
Make X a failure; all the code is correct.

It's counterintuitive, you should always prefer to classify X as a bug, as long as !X satisfies the criteria for preconditions:
It is possible to ensure !X.  For example, there's no way for the caller to ensure there's enough disk space to save a file, because other processes can use up any space that might have been free before the call.  So you can't make “there's enough disk to save” a precondition.
Ensuring !X is considerably less work than the work done by the callee.  For example, if the callee is deserializing a document and finds that it's corrupted, you can't make it a precondition that the file is well-formed, because determining whether it is or not is basically the same work as doing the deserialization.

## Definition

  Failure: inability to satisfy a postcondition in correct code.

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

## Two kinds of failures

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

### Interlude: Exceptions?

Way back in 1996 I embarked on a mission to dispel the widespread fear, loathing, and misunderstanding around exceptions.  Yes I'm old.  While I've seen some real progress on that over the years, I know some of you out there are still not all that comfortable with the idea. If you'll let me, I think I can help.

#### Just control flow

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

#### Also, type erasure

OK, I lied a little when I said exceptions are just control flow.  There's one other big difference between the exception version and the explicit version: the exception version erases the types of the failure data, and catch blocks are just big type switches with dynamic downcasts.

Lots of us are “static typing partisans,” so at first this might sound like a bad thing, but remember, as I said, none of the code propagating this failure (or even recovering from it usually) cares about its details.  What do you gain by threading all this failure information through your code?  When the reasons for failure change you end up creating a lot of churn in your codebase updating those types.

In fact, if you look carefully at the explicit signature, you'll see something that typically shows up when failure type information is included: people find a way to bypass that development friction.

fn serialize_section(s: Section) -> MaybeFailure<ArchiveFull,IOError,Unknown>

Here an “unknown” case was added that is basically a box for any failure type.  This is also a reason that systems with statically checked exception types are a bad idea.  Java's “checked exceptions” are a famously failed design because of this dynamic.

Swift recently added statically-typed error handling in spite of this lesson that should be well-understood to language designers, for reasons I don't understand.  There was great fanfare from the community, because, I suppose, everybody thinks they want more static type safety. I'm not optimistic that this time it's going to work out any better.

The moral of the story: sometimes dynamic polymorphism is the right answer.  Non-local error handling is a key example, and the design of most exception systems optimize for that.

### When (and when not) to use exceptions

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

## How to Handle Failure

OK, enough about exceptions.  Finally we come to the good part!  Seriously, this was originally going to be the focus of the entire talk.

Let's talk about the obligations of a failing function and of its caller.  What goes in the contract and what does each side need to do to ensure correctness?

### Callee

Documentation:
Document local failures and what they mean.
Document non-local failures at their source, but not where they are simply propagated. That information can be nice to have, but it also complicates contracts and is a burden to propagate and keep up-to-date.

Code:
Release any unmanaged resources you've allocated (e.g. close temporary file).

#### Optional

If mutating, consider giving the strong/transactional guarantee that if there is a failure, the function has no effects.

Only do this if it has no performance cost. Sometimes it just falls out of the implementation.  Sometimes you can get it by reordering the operations.  For example, if you do all the things that can fail before you mutate anything visible to clients, you've got it.

Don't pay a performance penalty to get it because not all clients need it and when composing parts all the needless overheads add up massively.

### Caller

- Discard any partially-completed mutations to program state or propagate the error and that responsibility to your caller.  This partially mutated state is meaningless.

What counts as state?  Data that can have an observable effect on the future behavior of your code.  Your log file doesn't count.

#### Implications as data structures scale up

The only strategy that really scales in practice, when mutation can fail, is to propagate responsibility for discarding partial mutations all the way to the top of the application.  That in turn implies mutating a copy of existing data and replacing the old copy only when mutation succeeds.  Either way, you probably end up with a persistent data structure (which is a confusing name—it has nothing to do with persistence in the usual sense).

A persistent data structure is one where a partial mutation of a copy shares a lot of storage with the original.  For example, in Photoshop, we store a separate document for each state in the undo history, but these copies share storage for any parts that weren't mutated between revisions.  This sharing behavior falls out naturally when you compose your data structure from copy-on-write parts.

### What (not) to do when an assertion fires.

- Don't remove the assertion because “without that the program works!”
- Don't complain to the owner of the assertion that they are crashing the program.
- Understand what kind of check is being performed
	- If it's a precondition check, fix your bug
	- If it's a self-check or postcondition check, talk to the code owner about why their assumptions might have been violated

### Probably different functions for unit testing.








Notes:
  - read from network, how much was read
    - no-error case exists
    - podcast
    - likely a local handling case.
    - don't go to vegas with something you're not prepared to lose.

Quickdraw GX: 15% performance penalty for making silent null checks.
