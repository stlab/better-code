# Errors

In the *Contracts* chapter you may have noticed we made this reference
to the concept of *errors*:

> If the preconditions are met, but the postconditions are not, and
> the function does not report an error, we'd say the method has a
> bug.

In the interest of progressive disclosure, we didn't look closely at
the idea, because behind that simple word lies a chapter's worth of
discussion.  Welcome to the *Errors* chapter!

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

We'll divide errors into three categories:

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

[^avoidable]: While bugs are inevitable, every *specific* bug is
    avoidable.

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
error means that the program can “sally forth entirely unscathed,”
i.e. that the program state is intact—its invariants are upheld.

Also, the state must make sense given the correct inputs received so
far. “Making sense” is necessarily a subjective judgement, so examples
are called for.

- The initial state of a compiler, before it has seen any input,
  certainly meets its invariants. But when an error is
  encountered, resuming with that state would ignore the context seen
  so far that can help inform further diagnostics.  If the following
  text did not match what is expected at the beginning of a source
  file, it would be flagged as an error.  We the error might, for
  example have been detected in some deeply (correctly) nested
  construct. If that state isn't preserved, each closing delimiter of
  that construct will be flagged as a new error.

- In a desktop graphics application, it's not enough that upon error
  (say, file creation fails), the user has a well-formed document; an
  empty document is not an acceptable result.  Leaving them with a
  well-formed document that is subtly changed from its state before
  the error would be especially bad.

These examples show that even if invariants are upheld, a program can
be very scathed indeed.

### What About Recovery From Bugs?

We've just seen an examples of recovery from an input error and a failure.
What would it mean to recover from a bug?

First, the bug needs to be detected.  As we saw in the previous
chapter, not all bugs are detectable. Also, it's important to admit
that when a runtime bug check fails, we're not detecting the bug
per-se: since bugs are flaws in *code*, finding bugs involves
analyzing the program.  We're really detecting a *downstream effect*
that the bug has on *data*, akin to the way physicists conclude from
cosmic microwave background radiation that the universe started with a
big bang.  We know something happened, but we don't know exactly where,
how or why.

Assuming we have a detectable bug, usually that means somebody's checking a precondition and that precondition check fails.
And that means there's a bug in the collar that caused them to pass an invalid argument.
So when that happens though, you're not really detecting the bug itself.
You're detecting one of its symptoms like some kind of a cosmic echo.

The bug itself occurred some indefinite point before that.
Right then, there's a series of logical conclusions that the the code may have made about what it had that are incorrect.
That led it to produce this input that you you see doesn't satisfy (preconditions,.
OK.
So can you Sally forth on scathed?
Well, the problem is you don't know, right?
Because of the bug, your program state could be very, very scathed indeed.
Umm.


Umm OK?
OK, so your program state if it's scathed selling 4th at this point is a terrible idea for lots of reasons.
So there's sort of two categories.
First, there are effects in the outside world.
I don't know.

Uh, so the users data might be corrupted, right?
And they might say that that way and they'll lose the last good state they had.
Right.
So that's that's pretty serious.
The other thing is, if you've done in a security evaluation, the assumptions that underlie that evaluation might be violated.
So by continuing, you may be opening a security hole and so it like sort of to sum up, you don't have enough information about the state of your system to do a recovery to to Sally forth reliably.
And you can't.
You also can't detect whether you've.
Recovered correctly, right?
There's there's nothing to look at and the penalties that we just talked about for failure to do it correctly are really, really high.
OK.
So that's one category, but then there's also the impact on the development process.
So if you Sally forth the bug is gonna be masked and we'll never get fixed until at some point, you know, somebody will observe the effects of this.
It's gonna affect your, your customers and your and if it you know when it affects the really important customer, your management may insist that you do something about it.
Right now all you'll have is evidence you don't remember.
You didn't detect the bug.
You don't have a detection of the bug.
You have some very distant echo in the users document that's corrupted and now now it's a long process to, you know, try to figure out where that corruption came from.
Right.
You're you've you've gotten the information very, very late.
Last of all, most code is correct, so you're “bug,” recovery code will never run.
Probably it certainly isn't gonna get tested.
I if it got tested, you're not gonna ship the tested one because you're gonna fix the.
You're gonna fix the problem right?
All of this recovery code bloats your program and every single line is a liability with no offsetting benefits.
So.
Yeah, I think this is.
This is an interesting insight.
I mean, they're do exist robust systems, right?
So they they can recover from bugs.
How do they do that?
Well, it's all.
It's almost always basically always.
It's outside the process, right?
Maybe the robustness of the system comes from redundancy.
You have you have three different processes and they all vote on the result.
The like this is the kind of thing you might see in like the F22 Joint Strike Fighter, right?
So yeah, there could be a bug.
First of all, they you know they check the code a lot more carefully than we do, but but they also put in safeguards in place so that so that if you know you have three systems voting on the result and one disagrees, you can kill that process and start it up again.
Umm.
So yeah, sometimes it's possible to design a system to recover from books, but don't expect to do it in in your process.
To sum up, uh in general you can't recover from bugs and it's a bad idea to try.
So what can you do?
Well, the way to handle bugs is to stop the program before any more damage is done and generate a crash report for debuggable image that captures as much information as you possibly can about the state of the program.
So there's a chance of fixing the bug.
Umm, be there might be some small emergency shutdown procedure.
You might need to perform like saving information about the failing command so your application can offer to retry it for you when you restart it.
Were you?
You know, maybe you can say something to the user about the reason that you're exiting.
So this is bad, right?
This is really bad if if you don't do something, really go out of your way to do something about it, it's gonna be experienced as a crash by the users, but it's the only way to prevent much worse consequences of a botched recovery attempt.
Remember the chances of battery are really high because you don't have enough information to do it reliably.
There is an upside, though, right?
It's also gonna be experienced as a crash by developers, QE teams and beta testers, and that gives you a chance to fix the bug, right?
It's not going to slip by those people unnoticed and then hit your customers in a really damaging way.
So you can though, mitigate this experience of of crashing right?
For example, you could say something to the user about the reasons that you're exiting, and you can actually make it sound pretty responsible. So.
So this is important.
You know, a lot of people have a hard time accepting the idea of voluntarily crashing or exiting right?
Exiting early is really what that should say, but you know we should face it.
You're bug detection isn't the only reason that the program might exit early, right?
You can crash from an undetected bug were a person can trip over the power cord, and really you should design your software so that when these bad things happen, they're not catastrophic.
In fact, you know, if we stop, you know, pushing, pushing bugs away and and early exit away.
As though as though it's an intolerable thing, we could actually embrace it and try to make it really seamless, right?
But you have to to do that.
You have to accept that early exits are sometimes gonna be a part of the whole package of user experience that you're trying to to deliver.
Umm.
Maybe you could arrange for the program to restart itself, for example.
Umm so.
In fact, there are platforms that actually force you to live under constraint of, you know, no early exit, right.
So on an iPhone or iPad, for example, to save battery and keep your foreground apps responsive, the OS might kill your process anytime it's in the background.
But it's going to make it look to the user like the the app is still running and when the user switches back, every app is supposed to complete the illusion by coming back up in the same state it was killed in.
I can tell you that as a user, it's really jarring when you encounter an app that doesn't do that, right?
So the point is resilience to early termination is something that you can and should design into the system.
So Photoshop uses a variety of strategies for this, so we already we always save documents into a new file and then atomically swap that file into place only after the save succeeds.
So we never crash, leaving some half written corrupted document on disk, right?
We also periodically save backups so you only had Most lose the last few minutes of work, but we could be more ambitious about this, right?
We, if we needed to tighten that up, we could maybe save a record of changes since the last fall back backup.
OK.
Umm, so the usual mechanism that we have for terminating a program when a bug is detected is called an assertion, and traditionally it's spelled, you know something like this and this spelling comes from C and C++.
If you're programming in in some other language, you probably have something similar and the the facility from C is pretty straightforward.
Either it's disabled, in which case it generates no code at all, even the.
Check is skipped.
Umm.
Or it does the check and exits immediately with a predefined error code if the check fails, usually printing a a message containing the text of the failed check and its location in source.
Good debuggers commonly stop at that assertion rather than just exiting, and even if you're not running in the debugger on many on Major OS's you'll get a crash report with the entire program state that could be loaded into a debugger.
So this is great for catching bugs early before they get shipped and and actually diagnosing them provided people use it.
And uh, so another important dynamic is the project's commonly disable assertions in release builds.
So this has the nice side effects of making programmers comfortable adding a lots of assertions because they know they're not gonna slow down the release build, and that means more bugs get caught early.
But unless you really believe you're shipping bug free software, you might wanna leave most assertions on and release builds.
So in in fact the security of your software might depend on it.
So if you're programming in an unsafe language like C, opportunities to cause undefined behavior are all around you, and when you can assert that the conditions for avoiding that you be are met before executing the dangerous operation, the program will come to a controlled stop instead of instead of opening an arbitrarily bad security hole.
Yeah, I should have.
I meant to to make this distinction earlier, right?
Exiting because of an assertion is not a crash, right?
This is a controlled stop for calculated reasons.
Umm so but the problem with leaving assertions on and release is that some checks are too expensive to ship.
And let's be honest, a lot of programmers are gonna go with their gut about what's too expensive instead of measuring.
So we really need a second expensive assert, right?
That is only on in debug builds, so we can continue to cache those bugs early.
And there's another problem with having just one assertion.
It doesn't Express sufficient intent.
There are lots of different reasons you might wanna be doing this kind of a check, so it might be a precondition check, right?
Or you're asserting functions author might just be double checking their own reasoning, and when these two different assertions fire, the meaning is really different.
The first one indicates a bug in the color and the other one is a bug in the callee, so I really wanna separate precondition and self check functions.
I want both of those.
Now, if I'm writing in a safe by default language like rust or swift, the checks that prevent undefined behavior like array bounds checks or special I can afford to turn off all of the other checks in shipping code.
But these checks are the ones that uphold the safety properties of my system.
Right.
And if I turn those off, the that's compromised.
So I wanna separate assertion for those for those checks that prevent undefined behavior even if I don't ever anticipate turning off the other ones in a shipped product, because these are the ones we can't delete from the code, right?
So you want to make that obvious by their spelling?
And furthermore, I'm I might wanna turn the others off locally so I can measure how much overhead they're incurring.
Alright, so I hope you get the idea.
I'm not trying to prescribe the exact set of assertion facilities your project needs, but at carefully engineered suite of these functions with properties appropriate to your project is part of a comprehensive strategy for dealing with bugs.
If you haven't gotten one of these, go design it.
OK.
So one last point about the C++ is Sir.
Umm, it's better than nothing, right?
But because it calls abort, there's no place to put any emergency shutdown measures.
So you can't even display a message to the user, so to the user if you use C's Cert, it's always gonna feel like a hard, unceremonious crash.
You probably won't fail to certains to call terminate instead of abort, right?
Because there are terminate handlers and those would run.
That gives you a chance to do some origin.
See shut down measures.
So that's another reason to engineer your own assertions, even if you're only engineering one.
OK, so at this point somebody always asks, but you know I I'm not allowed to terminate.
My manager says that that we have to keep running no matter what.
Right.
Umm, So what do you do?
Well, first, you've gotta fight for the right to park.
I need to terminate.
Right.
If you've got a critical system you wanna advocate creating some recovery system that's outside of the process because there is no reliable recovery inside the process.
And if you lose that fight today, right.
You wanna keep fighting, but in the meantime, fail as noisily as possible, preferably by when at least when you're not shipping the code, get it to terminate right and also set yourself up to deal with the day that that you win the fight because at some point the cost of of following this possible this policy are gonna become obvious.
And so that means use a suite of assertions that, well, today they don't terminate, but you can change their behavior when you do win the fight, OK.

I I don't know if we're going to get to the end because of the scope expansion anyway, so as much as we all love talking about bugs, it's time to leave bugs behind and talk about failures.

So let's say you identify a condition where your function is unable to fulfill its primary purpose, so that can occur in one of two ways.
Either something you're function calls has a precondition that you can't be sure you're prepared to satisfy, or something you're function calls. Itself.
Reports the failure to you so usually have two choices at this point.
So one is you can say that your inability to make progress reflects a bug in the caller, right?
You can make not XD be a precondition of your function or you can make X failure right, which means that all of the code in the system is correct.
Umm, that's counterintuitive, but you should actually always prefer to classify that situation as a bug in the caller, as long as it satisfies the criteria for acceptable (preconditions,.
So there there are a few things you need to satisfy, right?
It needs to be possible for the caller to ensure the condition, right?
There's no way for the caller to ensure there's enough disk space to save a file, because other processes can come and use up any space that might have been free before the call.
So you can't make there's enough disk to save a precondition.
The the other way in which something might not be a suitable precondition is if it takes as much work for the caller to ensure it as the work you're gonna do in in performing the operation in the end anyway.
So for example, if if they're deserializing a document, umm and you find that it's corrupted, you can't make it a precondition that the file is well formed, because determining whether it's well formed or not is the same work that as doing the deserialization so.
OK, so prefer to make it a precondition, but.
If you can't satisfy a post condition and you're incorrect code, you're in correct code.
That's a failure.
So why am I tying this definition to postconditions, other than to bind our understanding of Error Handling to under to the way we understand correctness?
That's a valuable thing, but there's there are more reasons.
So first of all, it's simplifies and improves understandability of contracts.
So this is really easiest to see if you have a dedicated mechanism in the language for Error Handling, so I just.
I'm using fictional programming language here.
There should be easy to understand what's happening though.
Here's here's a couple of examples.
So in the first case we have we have the the error cases treated as though it's part of the post condition, right?
We have to say.
This thing returns X sorted or it throws an exception in case something fails, right?
You're going to end up saying that a lot if it's not part of the post condition.
You can say this now if you you know you know it's throwing an exception, you know that means the operation failed.
There's nothing else you need to say, even if you do feel you need to say something about possible failures, that becomes a secondary note.
That's not essential to the contract, right?
You get something like this?
In in both of these cases, a programmer can know everything essential from that summary fragment at the top and the signature of the function.
So another way this separation plays nicely with exceptions is that you can say that the post condition of a function describes what you get when it returns, and a throwing function never returns.
OK.
But if you don't use exceptions., you still get simplified contracts from this, as long as you have a dedicated type to represent the possibility of failure.
So here's here's an example.
You can say that this returns X in sorted order because you know that result or failure means or.
You know, there's the possibility that the operation failed and I'm reporting that, umm.
Separating this the primary intention from the reasons for failure makes sense because the reasons for failure actually matter less.
And if that's not obvious to you yet, some justification is coming.
So finally another reason to exclude this failure case from the post condition is that you want postconditions, to be solid and fully described.
But when a mutating operation fails, it often leaves behind a state.
That's very nebulous, and as I said in the contracts talk, you usually don't want to describe it because it's detailed that nobody cares about.
But if it's part of the post condition you you end up, you need to say something about it and that further complicates the contracts.
So you end up with something like this.
OK, this sorts of Xia cording to order or throws an exception to Forder fails, leaving X modified in unspecified ways and you end up saying something like that over and over again for mutating operations instead of just being able to say.
Swartz X according to order.
OK.
Now if you spend some time writing code that that handles errors carefully and correctly, especially in a language like C where all of the error propagation is explicit, failures start to sort of sort themselves into two categories.
There's local failures and non local failures based on where the recovery is likely to happen.
Local recovery.
It occurs very close to the source of the failure, usually in the immediate caller, in a way that often depends heavily on the reasons for the failure.
So in many cases, also in, it tends to be more in performance critical code.
So for example, you might have an ultra fast memory allocation memory allocator that draws from a local pool.
That's much smaller than system memory, and on top of it you build a general purpose allocator and first tries your fast allocator, and only if that allocation fails, it recovers by trying the system allocator.
Right, that's very local Handling.
You're gonna try the fast allocator and try your alternative method and the error doesn't propagate any further than that.
Umm, another common example is the lowest level function that tries to send a network packet can fill for a whole slew of reasons, and you can look these up in the in the POSIX documentation.
Some of these indicated temporary condition like packet collision and 99% of the time the immediate caller of this low level function is a higher level function that checks for these conditions and if it finds one of these temporary conditions, it initiates a retry protocol with exponential backoff and only itself fails after about, you know some number of failed retries that lowest level failure is local and the failure after and retries is very likely to be nonlocal, so nonlocal recovery nonlocal recovery is far far more common, umm, and it usually it occurs far from the source usually.
In a way that doesn't depend on the details of the reason for failure.
For example, when you're serializing a complex document, serializing any part means serializing all of that all of the subparts and parts are ultimately nested many layers deep, right?
And because you can run out of space in the serialization medium, every step of the process can fail.
So if you write out the error propagation explicitly, it usually looks something like this.
Right.
You have it error code and then this pattern gets repeated over and over again.
Each part you serialize it and check to see if there was a failure and if there was a failure you you have an early return. Umm.
So after every operation that can fail, you're you're logically adding and if there was a failure, return it OK and so there are many layers of this propagation, and none of it depends on the details of the reasons for failure, whether the disk is full, or the OS detects directory corruption or the serialization is going to an in memory archive and you run out of memory, you're going to do the same thing.
Finally, we're the propagation stops and the failure is ultimately handled.
Like let's say this is a desktop app.
Again, the recovery is usually the same no matter what the reasons are for the failure you report the problem to the user and you wait for the next command.
OK, so let's talk about exceptions for a minute.
Way back in 1996, I sort of developed a personal personal mission to dispel the widespread fear, loathing, and misunderstanding around exceptions.
So yeah, I'm old.
Ohh and while I've seen some real progress on that over the years, I know that some of you out there are still not all that comfortable with the idea of exceptions, and if you'll let me, I think I can help the the first point to know is that exceptions are just control flow and you can see the motivation for for this really easily with cases like this one, because using an exception eliminates the boilerplate and lets you see the codes primary intent right there.
There is no magic here.
Exceptions.
Just like a Switch statement exceptions.
Capture this commonly needed control flow pattern and eliminate unneeded syntax so to to grok the meaning of this code in its full detail, you mentally add and if there was a failure, return it just that same thing that we said we were gonna repeat over and over again in the code with the explicit error handling everywhere.
But if you push failures out of your mind for a moment, you can see how the function also is much more easy to see how it fulfills its primary purpose, right?
That that primary purpose was a lot was obscured by all of the failure handling in the earlier version, and this effect of of clarifying the primary purpose is even stronger when there's some control flow that isn't related to error handling, because the the pattern is less.
You know the pattern of stuff that you can ignore is less obvious, OK?
Umm OK, so I said exceptions.
Are just control flow.
I I lied a little bit.
OK, there's one other big difference between the exception version and the explicit version.
The exception version of erases the types of the failure data and catch blocks are just big type switches with dynamic down casts that recover that information.
So a lot of us are static typing partisans, so at first this, you know, erasing this type information might sound like a bad thing.
But remember, as I said, none of the code propagating this failure or even recovering from it, usually cares about the details of the reason for the failure.
They don't care about the the data in the fail failure report.
What do you gain by threading all that failure information type information through your code when the reasons for failure change, you end up creating lots of churn in your code base.
Updating this types.
In fact, if you look carefully at the explicit signature.
You'll see something that typically shows up in systems where failure type information is included.
People find a way to bypass that the development friction induced by static types right here we have this unknown case, and that's basically a type of raised box for any failure type.
This is also a reason that systems with statically checked exception types are a bad idea, but it doesn't matter whether you're doing exception handling or reporting errors another way.
The same dynamic occurs.
Java has a feature called checked exceptions, which is a famously failed design.
Because of this dynamic people.
Having to bypass it.
Swift recently added statically typed Error Handling.
In spite of this lesson, that should be well understood to the language designers, I I don't understand why there was a lot of fanfare from the Community, because I suppose everybody thinks they want more static type safety.
But I'm not optimistic that this time it's gonna work out any better than I did for Java.
So the moral of the story here is sometimes dynamic polymorphism is the right answer, and nonlocal error handling is a great example of that, and the design of most exception systems optimized for that.
OK, unfortunately we are getting right to the limit on time, so.
Yeah, like there's a we're not gonna get to the end today.
So I think we're gonna.
We're gonna need to have a part too.

Todd Baumeister   50:51
Alright, I'll be in the brave idiot who goes first.

Nick DeMarco   50:55
Thank you, Todd.

Todd Baumeister   50:56
Ah, awesome presentation.
Thank you.
Umm.
As a former C developer, although I don't if I can say former, can you ever forget how to writing a bike?
It was really good and a lot of really good points about Error Handling, but.
I have to ask so the conditions you're looking for are like the worst case.
Like we we can't recover from them.
And you, you mentioned the uh inheritance or the I can't remember the exact words you use, but the idea that you can have a a chain of handlers when an exception comes out and filter through that and then hit an all at the end.
So can I summarize your talk to?


Todd Baumeister   51:44
As a developer, I have expected errors.
Yes, things that I expect to potentially go wrong.
I like for example, my network times out.
I need to handle that, but we always need a catch all at the end for.
Well, no, we should not have a catch all at the end for uh, the unexpected errors is that my main takeaway from here or.

Dave Abrahams   52:08
Umm.
If I understand, yeah, if I understand your question right.
Uh, no, I'm not saying that.
Umm, let me ooh.
Let me be let me try to sort some of this out though.
There's a lot of good stuff in your question.
Umm.
So umm, remember from the beginning unexpected errors that you almost always means bugs.
OK.
And and part of my advice.
Well, which we we didn't get to, but.
It's right here.

Don't use exceptions for bugs when a bug is detected, you should exit the program, not throw.
Don't worry about catching.
Certainly don't use exceptions to exit the program, right?
I know that's the default behavior if you don't catch it, but the problem with that is anybody up the chain from you?
I'm going to just read what I've got here.
The default behavior of exceptions.
Has stopped the program but throwing when you find a bug defers the choice about to whether whether to actually stop to every function above you in the call stack, and that is not the service that is a burden.
Right, giving giving your clients bad choices to make does not help anybody.
So if you made your function harder to use by giving your client just more decisions to make.
If you do that.
OK.
So then so last, OK, what about what about catchall case at the top anyway, right?
Maybe.
Maybe it's not for bugs, maybe it's for some exception type that you don't you you want to wear of at the top level.

Todd Baumeister   54:09
Yourerunning.net on the C++ platform and .net through exception and you gotta catch it someplace.

Dave Abrahams   54:15
Yeah.

Todd Baumeister   54:16
That's where I've experienced this, yeah.

Dave Abrahams   54:18
Yeah.
OK.
So I mean, let's let's talk about the the desktop app.
Uh, OK, because that's something I I can I can address easily.
We can look at other examples.
So you got an unidentifiable error, but it it prevented your operation from succeeding.
So what's the problem here?
If you don't know anything about the exception type at all, you can't really give a meaningful error report to the user.
That's the worst.
That's the worst part of it.
That's that's really so you have to say sorry and unknown error occurred.
That's embarrassing, but it's not.
It's not catastrophic, right?
You can from there you can proceed just as though any other thing like ran out of disk space occur.

Todd Baumeister   55:15
OK.
Thank you.
Yes, helpful.

Nick DeMarco   55:20
Dustin, you wanna go ahead?

Dustin Passofaro   55:22
And the last 30 seconds I'm.
I'm sitting at the top of this bell curve of my relationship with exceptions.
You start out with ohh.
Exceptions are cool.
Ohh my gosh, never use exceptions.
They are the bane of my existence.
Why oh why?
And I see you over here and you're starting to push me over the edge to wait a minute.
Maybe there is something and I'm not one over yet, because I still see and please I want to be one over.
Please help me continue to see how this doesn't just lead to the most mind boggling spaghetti.

Oliver Unter Ecker   55:51
Can you talk with the office?
I could.

Dustin Passofaro   55:54
Or and and.
Sorry, somebody else is talking.

Dave Abrahams   55:56
OK.

Dustin Passofaro   55:57
So to kind of double down, I still see even in the cases where it's like, oh, this is a known error, you're still deferring and now you have your entire call stack above you.
Oh, is it my responsibility?
How about yours?
How about yours?
That's the first problem I see.

Dave Abrahams   56:13
OK.
Well, let me address that to start with, if you if you do Error Handling carefully, no matter what mechanism you use, that pattern comes up.

Dustin Passofaro   56:26
Good observation.

Dave Abrahams   56:27
OK.

Dustin Passofaro   56:27
OK.

Dave Abrahams   56:27
So.

Dustin Passofaro   56:27
Yeah, I see that.

Dave Abrahams   56:28
So it's just, it's just a mechanism, it doesn't change the nature of failure handling, which is the same no matter what mechanism you use.

Dustin Passofaro   56:38
That's the light bulb, OK?

Dave Abrahams   56:40
OK.

Todd Baumeister   56:40
We can.
I just add the big difference here is known versus unknown, right?
You're talking about known exception handling versus you're talking about unknown, which is a bug, and it's out of no.

Dave Abrahams   56:52
Uh, yeah, yeah, let me, I, I, I wanna be really precise here.
OK so so I prefer not to use the word unknown because a library could throw could give throw you a failure, right?
That doesn't represent a bug, but they didn't tell you about the type.
They didn't tell you they were going to throw that type.
So an unknown unknown exception is not a is not a bug.

Todd Baumeister   57:25
I a structured exception is that we mean like umm.
An application exception.
Let me put it that way versus like a null pointer someplace, yeah.

Dave Abrahams   57:37
OK.
So yeah, there there's this unfortunate.
So.
So yes, what I'm talking about are language feature exceptions.
OK, there are.
Ohh.
Unfortunately, uh.
So lots of systems and and processors call things like divide by zero and exception, but they don't.
They don't act like exceptions.
In languages that propagate up the call stack and and take care of things like destructors.

Todd Baumeister   58:08
What?
What's so system interrupts first application errors?

Dave Abrahams   58:13
Sorry. What?

Todd Baumeister   58:13
Maybe then system enter ups for application errors like divide by zeros to the system interrupt.

Dave Abrahams   58:20
OK, the problem again.
Let's let's be precise.
In our language you say application error.
Given what we saw about errors, that could just mean a bug in the logic of the application.
So don't handle that with an exception if the if something you're using throws an exception at you for those cases, which is a common Miss Design, C has it even in places there, right?
Stop it.
Turn it into an assertion failure.
You don't want your your unrecoverable code paths mixed with your recoverable code paths, right?

Todd Baumeister   59:06
Thank you.

Nick DeMarco   59:09
I have a question from Kevin Hopps as I sense a cadence here.

Dave Abrahams   59:12
OK.

Nick DeMarco   59:14
Incidentally, as I've seen a clapping emoji, if you have to drop off, feel free to.
But we like to go with the Q&A section for as long as folks are interested or until someone gets exhausted.
So we're gonna go for a little bit longer.
Also, Please note that I've just dropped a survey link in the chat, so if you do drop off, please take a like the five minutes that it takes to answer the questions we recently made all of the questions not required, so if you just wanna tell us one thing about the talk, you can do that now.
So don't feel obligated to fill out every single question, but Kevin asks how should I write my utility function?
Take open file for example.
It might be fatal for one caller and error for another caller.
We're not even an error for yet another caller.

Dave Abrahams   1:00:02
OK.
So does it?
That's a great question.
Umm, so if it's not necessarily fatal, right?
If if you want to make this thing useful to everybody, obviously you can't make the decision to make it fatal, right?
So so.
You have to.
You have to report the condition to to your caller.
Now remember what I said about about contracts and.
Contracts and and whether you decide something as an error or not.
Well, it's actually.
All right, listen, let's let's back up first and and classify this.
This is this is a not a bug error right?
No, you you can't.
Nobody's in a position to control whether open a file is gonna succeed, right?
So so clearly it's not a bug, it's a failure of some kind, right?

Kevin Hopps   1:01:13
Might be a bug if the call if the call to open the file is from a piece of code that knows that file should be there, then it's a bug.

Dave Abrahams   1:01:25
What do you mean should be there?

Kevin Hopps   1:01:28
If you say always create a log file when you start the program and later you try to open that log file and it's not there, that could be a bug.

Dave Abrahams   1:01:40
Well, not a bugging your code.

Kevin Hopps   1:01:46
Well, maybe I've come up with a poor example.
The point is, only the caller knows whether the result is a bug or not.
I mean it, it might be a bug in some context and not a bug in another context.

Dave Abrahams   1:01:59
Fine.
Fine.
If if to here in general, if only the caller knows you can't make a, you can't make a catastrophic decision, right?
It's the same as not knowing whether it's fatal, right?

Kevin Hopps   1:02:14
Right.

Dave Abrahams   1:02:15
Actually, bugs are fatal.
We've just, we've said that right, bugs are gonna be fatal.
So so if you don't know whether it's going to be fatal for the client, you can't make the decision that is fatal.
So you can treat it as a post condition failure, right?
So what's the?
Was the other possibility.
It's not an error for another caller.
I'm not sure what that means, like whether it's an error in your, you're the open file function, whether it's an error in the open file function is not up to the caller, right?
The the caller may decide.
Ohh, I'm gonna deal with the failure to open the file some other way, but it's still a failure of the open file function, right?
Maybe it's maybe the caller is not gonna propagate that failure to its caller.
Maybe it's got some alternative way to achieve success, but it would still an error in the scope of the open file function.
I hope that answers the question, Kevin.

Kevin Hopps   1:03:24
Yes, thank you.

Dave Abrahams   1:03:26
Sure.

Nick DeMarco   1:03:34
Not seeing other questions in the chat, although I do wanna call out that Florin shared something very interesting about Erlang that I invite folks to read if they're curious.
Describes it as a nice complement to the concepts that Dave presented today, and I'm inclined to agree.
Having skimmed it twice now, but we are now a little bit over time.
I saw someone just come on camera Learn.
Maybe you wanna comment a little bit about Erlang and what you shared.

Florin Trofin   1:04:03
Umm.
Yes.
Umm, I highly recommend for engineers to read that paper because I think I I mean you can skip over the airline itself.
The language is not my favorite language, but the runtime system.
It's remarkable and some of the properties that it has, for example, you know it, it had like a an astounding, I don't remember like 7 nines of like it's been running for years and decades without stopping it and being able to patch the system at runtime without shutting it down.
I mean only those two properties.
If I tell you like that, that should raise an eyebrow and say, OK, well, that's something.
And it was done in the 70s, right?
So it's like ohh way back, but the principles I think they're very sound and the principles have been validated by, you know, these remarkable traits that these systems have these switches, these telephone switches that they've been running for decades and the supervision concept that it's introduced an airline, it's very powerful.
So the idea is that basically when you want to do something that's not trivial.
So if it's any complexity, then you delegate to a child subprocess, and in Neverland the processes are not like the OS processes.
There's something very much cheaper than that.
So you can spawn millions of processes and a nice property of the system.
Is that also establishes a bidirectional link between the parent and the the children that you're spawning?
So if a child so you, you you you need to do something.
And so you you delegate to a child or multiple children for example, you can spawn a bunch of children.
And let's say one of them fails.
Then you immediately get notified that that particular thing fails, and you as a parent can have different policies.
For example, you can say I wanna respond that node, you know a retry it or I can respond all the nodes that were even though it was only one child.
You know, because they kind of like altogether and it doesn't make sense to respond just that node and need to retry the whole thing.
And then if I fail doing that, then I report back to my parents.
So then simpler and simpler things get done.
You know, until like the whole system restarts, right?
It like restarts automatically, so that's a very interesting thought.
And you know, I've.
I've been thinking about that for a long time and I think his specially for distributed systems and services that makes has a lot of appeal, but I don't think it should be limited just to distributed systems.
I think it's also powerful when you think about normal software like desktop software.

Nick DeMarco   1:06:37
Hmm.
Dave, your thoughts?

Dave Abrahams   1:06:42
Umm yeah, I guess about that.
I I was wondering Florian, when you described those failures.
Umm, are those are those indeed failures the way the way I've described them in this presentation i.e.
Not bugs or or.
If they're or are these sometimes bugs?

Florin Trofin   1:07:05
So the plan, the paper actually does make a distinction, and it talks about like, what's the difference between an exception error or a failure and a bug.
And it's, I think a lot of your talk it uh, it overlaps with some of the concepts that are in there.
So that's why I said it's kind of like a nice complement to what you already discussed there.
I would be curious to hear your thoughts.
Maybe next time, you know, after you read the paper, you know there.

Dave Abrahams   1:07:31
Yeah, I'll read it before Part 2.

Florin Trofin   1:07:32
And because I also find it that it's it's it's it's really well written and well organized.

Dave Abrahams   1:07:34
That's a great idea.

Florin Trofin   1:07:39
As you know, the author organized their thought, his thoughts in the in the very well manner, so.

Dave Abrahams   1:07:44
So.
So it's better than the Erlang movies.
Have you seen their long movies?

Florin Trofin   1:07:50
No.

Dave Abrahams   1:07:51
Ohh there you can look them up on YouTube.
They're they're kind of hilarious.

Florin Trofin   1:07:56
OK.

Dave Abrahams   1:07:58
Yeah.
What else?

Nick DeMarco   1:08:09
All right.

Dave Abrahams   1:08:10
Anything else?

Nick DeMarco   1:08:11
What else?
I was just giving folks a moment.
But I think I think we might be reaching a cadence here.
So thank you to everyone that came.
Thank you to the 28 of you that that are sticking around for the discussion.
That's always fun, and I'm going to share a link in the chat one more time just to please take a survey.
If you've got a couple of minutes, let us know what you think.
Let us know in particular what you thought of the reading text on a screen narrative presentation style.
That's a first for us and I'm curious to see how it was in terms of communicating ideas and and understandability and things like that.
So please share your thoughts, but for now I guess let's wrap this up.
I'll see you next month for type design with Sean Parent.
That should be fun, but for now, enjoy your long weekend and we'll see you the next one.
Thanks everyone I.

Florin Trofin   1:08:58
OK.
Thank you for organizing these and thank you, Dave, for for your presentation.

Dave Abrahams   1:08:59
Thank you everybody.

Nick DeMarco   1:09:03
I agree.

Speaker 1   1:09:03
Thank you.

Nick DeMarco   1:09:03
Big kudos today if this was a lot of fun.

Dave Abrahams   1:09:05
Thanks, bye.

Nick DeMarco   1:09:06
File.

Nick DeMarco stopped transcription

## PART 2 ##

Alright, welcome back everybody.
Umm.
So just to refresh where we where well, first of all, for those of you who who don't remember part one or weren't here, umm this is a very slick presentation where I show you no slides and just this document that I wrote up with my notes is is in the background cuz it contains some examples which I'll no want you to look at.
Umm, so where we were at, we were talking about exceptions and I just wanna review a few things just for background.
You know, I tried to.
I tried to demystify exceptions.
A little bit there.
They're just a control flow mechanism.
I and and they don't introduce any new.
Problems to error handling, but if you're Handling errors right, you have basically all the same issues to to think about whether you're using return types or not, but they they do optimize for.
For things a little differently, they optimize for nonlocal error handling right where, where it's very likely that your immediate caller doesn't have anything to do with the error, and they're just gonna need to propagate it up.
And they also optimized for the they tend to to erase the types of error information in, which tends to prevent, uh, code churn has has different kinds of errors end up propagated through the code and just turns out to be a good thing for for most code, which mostly doesn't care about, uh, about what types you've actually got in the.
In the air, this cause most of the code is just propagating OK.
So and we were about to talk about Wendy's exceptions and when not to.
OK.
And I wanna start by by piercing some of the the aphorisms you may have heard about this because there's a lot of really nice sounding advice about when to use exceptions.
That's either meaningless or really vague, so like, use exceptions for exceptional conditions, right?
Well, how do I measure what's an exceptional condition?
I don't know.
Don't use exceptions for control flow.
That one specifically.
I know that's really popular around Adobe and even appears in our one of our coding guidelines documents, but come on, if you're using exceptions, you're using them for control flow because that's what it is, right?
Umm exceptions.
Change which code executes next.
So I hope I can improve on that advice a little bit.
So umm, first of all, you can use exceptions for things that aren't obviously failures.
Umm so for example, when the user cancels a command, an exception is appropriate here because the control flow pattern is identical to the one where the command runs out of disk space.
For example, the condition ends up propagated to the top level.
OK.
Umm, uh.
And in this case, the recovery is just very slightly different, right?
There's nothing to report to the user when they cancel, but all the intermediate levels between the point where the failure is initiated and the point at the top of your event loop are the same.
So it would be silly to explicitly propagate cancellation using some other mechanism in parallel with the implicit propagation of failures that you get from exceptions.
So uh, but if you make the choice to to use exceptions to deal with user cancellation, I would strongly urge you to in your in your thinking and in your terminology classify this case as a failure, right?
I said it's OK to use exceptions for things that aren't obviously failures, but you can call this a failure.
Otherwise, if you don't do that, you're gonna undo all of the benefits you've got by separating failures from postconditions,.
Right.
And you'll have to include unless the user cancels, in which case you know an exception is thrown in the description of all of the functions that it could be cancelled, right?
So in the end, my broad advice is only use exceptions for failures, but be open minded about what you call a failure.
Actually, even if you're not using exceptions, any condition whose control flow follows the same path as nonlocal failures should probably be classified as a failure.
OK.
Umm, another prime example of a non obvious place to use exceptions is the discovery of a syntax error and some input right in the general case you're parsing this input out of a file and IO failures can occur, and Wilf and what's gonna happen, right?
If you have some nested call stack where you're, you've got a recursive descent for service.
Say umm uh.
When you hit this IO error, the control flow is going to be the same as the control flow.
When you hit a syntax error.
So if you call the syntax error, the failure of the parsing routine and use the same error reporting mechanism you you have a win for your code.
OK.
So those are some places where you can use exceptions next when not to use them right?
Don't use exceptions for bugs when a bug is detected, the program can't proceed reliably, right?
And what happens when you throw?
Well, there is a whole set of unwinding actions that happen.
It destroys things on the stack.
It changes where the stack pointer is and all of that happens before your debugger were your crash report.
If if you even get one occurs, right?
So you're destroying valuable information that you might need to find a bug.
Furthermore, anything that you do that's extra once a budget is reported is that much more likely to cause a problem.
Maybe maybe corrupt your document.
Open security hold and finally it can hide the bug from developers because after all, when you throw an exception that delegates responsibility for how to deal with it to your callers and your callers, maybe you know don't feel like stopping the application, right?
Maybe they wanna swallow the exception and continue that.
As I said before, it is not a service to delegate that choice to your to your callers.
It's a burden, right?
Don't don't give your your clients extra decisions to make the specially not don't open the door to bad decisions like continuing after a bug is detected, so you've just make your function that much harder to use.
OK.
So another thing that, yeah.

David Sankel   9:20
It looks like there's a a question in the chat Dinesh, you wanna go ahead?

Dinesh Agarwal   9:24
Yeah.
OK.
Thank you.
So I just had a quick question.
So Dave, you mentioned that if it detect a bug, please don't pass it as exception.
But while the code is in production, ideally the bug would translate as an exception.
I really don't understand that.
What exactly it means to like detect a bug if a developer is detecting a bug, they will try to fix it, right?

Dave Abrahams   9:53
Uh, OK, so you said a few different things that I guess need to be responded to if the developer has.

Dinesh Agarwal   10:00
Yeah. OK.

Dave Abrahams   10:01
So let's let me respond to the last thing first.
Cause that one easy if the developer detects a bug, ideally they would try to fix it.
Yes, I agree.
OK.
So then about production, so we were you were you present for part one of the talk?

Dinesh Agarwal   10:19
I joined 5 minutes late.

Dave Abrahams   10:21
OK, so so I pretty sure that we covered this in part one.
So once a bug is detected, if you continue to run, you increase the chance that you silently corrupt the users data in an unrecoverable way, right?
So for example, let's you can take Photoshop, which periodically saves document to recovery files you have.
You know, even there are more sophisticated systems that will also dribble out the commands that have executed successfully so far, so that you so that the application can replay them regardless.
You know that that's a solid state before the before the bug is detected, or at least there's a very high likelihood once the bug is detected.
Now you're proceeding based on incorrect assumptions and what can very easily happen is that those incorrect assumptions lead to corruption and the document that the user doesn't see, so they they proceed and then they save their document and it's all over, right?
You can never get that.

Dinesh Agarwal   11:36
Got it.
I see.
I see.
Cool.
Thank you.
Got it.

Dave Abrahams   11:43
OK.

Dustin Passofaro   11:44
I'm can I can I step in there too?
Because I think I'm also not understanding I I I shared his question actually and I was here for part one, so maybe I missed, maybe I wasn't understanding something there.

Dave Abrahams   11:47
Sure.
Yeah, you were.
I remember you.

Dustin Passofaro   11:56
Ah, good.
That's good.

Dave Abrahams   11:58
Yeah, you had good questions, so.

Dustin Passofaro   11:59
Umm well or yeah I I hope.
I hope this question is is also memorable, but we'll see.
I was also thinking sometimes a bug will come up and we'll we'll present itself as an exception.
Umm and awesome that I'll let you keep going.

Dave Abrahams   12:14
That's my next point.
Yes.
So as it says Ohh my my finger doesn't quite reach it, I can scroll it down right right there.
If you use components that misguidedly throw things like logic errors or domain errors or invalid arguments at you, those things all represent bugs.
Don't let those exceptions propagate.
Catch them and terminate the application.
Otherwise, you're just doing.
You're just essentially indirectly doing what we've just said is a bad idea.
OK umm now.
Uh, there are some systems like Python.

Dinesh Agarwal   13:05
It's so you didn't run, but it's a very interesting statement.
Like we understand that there is some misguided code in the uh code base.
Is there any guidance or is there any guidelines how how do we decide it's misguided a function or maybe code piece of code?

Dave Abrahams   13:27
OK, well this this is a very simple criterion if the code.
Response to bugs, in other words, misuse of the code right precondition violations by throwing exception.
That's misguided.

Dinesh Agarwal   13:49
But that we would know once we basically run it multiple times and basically let's say if there is a library that is getting loaded, we have not run it multiple times.
It's dynamic library.
In that case, is there any guidance would you like to share some?
Maybe sanity.
Shall we do some sanity for that code before relying on that? Ohh.

Dave Abrahams   14:13
Known OK so.
So I you know, I probably shouldn't assume this but but my basic my basic assumption is that the components that you use have documented APIs APIs.
OK, so that means they, you know, they tell you what they're going to do. Umm.
Although you know when there's a preconditioned failure, there are obligations to do things.
There are no obligations to do anything, so I guess discovering what you know, discovering these misguided uh things.
Uh probably ends up having to be a product of auditing or or, you know, when you observe these, these kinds of misguided exceptions during runtime.

Dinesh Agarwal   15:09
Got it.

Dave Abrahams   15:09
Umm so yeah.

Sean Parent   15:14
Or comment that your list there is is pretty good and you know a lot of people will just inherit from student logic error.
Uh.
For for anything that's a bug, and so.
So that's a good case if you're.
If you catch a Sood logic error.
You might want to treat it you know, as as fatal all the places in Photoshop where it puts up a dialog box that says a program error has occurred.
Umm, it's fine to tell the user that, but the next thing should be save out or recovery document and exit so.

Dave Abrahams   15:50
Umm yeah.
That said, I mean you shouldn't.
You shouldn't make the assumption that every component you're you use is going to be misguided, right?
Then you'll then you'll have try catch blocks all over the place and basically try catch blocks if you.
If you write your code right, should be extremely rare, mostly only at the top level.
Some you know the exception is.
Sometimes you have an otherwise an unmanaged resource and you need to clean it up.
So usually you can deal with that by managing it in a destructor, but something like you're initializing on initialized memory and you know an exception is thrown while you're doing that.
You might need a cache block to go and denialist all of the elements you've initialized, right?
So very rare.
OK.
Umm.
And all that said, I want to also acknowledge that there are some.
There are some systems like Python where using exceptions to report bugs is just part of the fabric of the system, right?
In fact, in Python they use exceptions to exit loops, which is.
As a little while arming to some people, but in Python you just you can't use this rule that that if you see one of these things you you stop the program.
You have to let it propagate.
OK.
Umm.
And there's a hand.

Josep Valls   17:33
Hi, yes, I think I was for so I mostly programming Python so that that's me but even in Java when network is in place there are lots of things that are very commonly reported exception but by means train libraries, anything from time out to to access like temporary resource access.

Dave Abrahams   17:34
Shouldn't.
Are those bugs?

Josep Valls   17:58
So, but those are the bugs.
But these these exceptions seems to be handled in a trackage, so we have lots.

Dave Abrahams   18:05
No.
Well, yeah, not not immediately, right.
So generally the pattern is there's some place, so remember, exceptions are for nonlocal error handling, right?
That they are generally for things that can't be responded to by the immediate caller.
So generally in the general case, the pattern is there's one try catch block, sort of at the top level of the application that that catches all of the things that propagate out of operations that fit.

Josep Valls   18:51
But simple things like a retry.
Will there be a good excuse for an exception to where the library throws a?

Dave Abrahams   18:57
Yeah.
Right.
Yeah.
So so if you have to retry a network operation now, right.
So that's what I'm what I've been calling a local failure and you might have a component that misguidedly uses exceptions to report local failures, in which case, yes, you do need a local Tri catch.
But as I also said in the previous section, local failures are are far and away much more rare than nonlocal failures.
There's there's just a few low level functions that that need to report local failures, so if you have, if you get a a component that reports a local failure with an exception, what you can do is put a little wrapper around it and use that wrapper everywhere.
Make that wrapper report the error differently.
So which is going to be my next piece of advice is don't use exceptions for local failures.
They're not optimized for that.

Josep Valls   20:13
Yeah.

Dave Abrahams   20:13
Does that help?

Josep Valls   20:15
Yes, I guess I'll get more context.
When after thought process things.

Dave Abrahams   20:22
OK, we can come back to that.
There will be time for questions at the end.
Are there other hands that we should deal with?

David Sankel   20:30
We've got one more hand in the queue, is he?

Izzy Muerte   20:32
Yeah, so this isn't actually a question, just a small note that in the same shift in philosophy, people are mentioning in the chat, Python has also been moving towards the approach of we shouldn't be throwing exceptions everywhere.
And so in recent versions of Python, they've made optimizations to the internal compiler for C Python runtime to not actually throw the, you know, stop, stop, loop, or stop iteration error, and the other ones that are used for control logic, as in more recent years, they've discovered ways to optimize it.
So they're actually starting to shift away from that.
They can't get rid of that behavior, unfortunately, because of 30 plus years. If that behavior.
So, but that's a that's the worst case scenario.
Fall back for what happens now in Python.

Dave Abrahams   21:26
That's good to know.
Umm yeah, I I strongly suspect there are also not separating the bug case from the from the failure case.
Umm.
So they're gonna keep reporting, you know, invalid arguments and and other bugs to you using exceptions.

Izzy Muerte   21:48
Umm that has been discouraged for new types that go into the Python's dead Lib.
There's still like some functions in the Python stdlib that's still do that, umm, but you'll see more of like a types integer error like if you pass the wrong number of arguments, obviously or like an assertion error.

Dave Abrahams   22:03
It.

Izzy Muerte   22:05
Rarely these days you get a value error except for like the built in types because they just had those four for decades at this point.

Dave Abrahams   22:11
Yeah.
So, so from the perspective of what I'm saying in this talk type signature error and argument Error, all of those things are equivalent.
They're they're exceptions thrown to indicate, you know, precondition failures, failures of the of the caller to do the right thing. Umm.

Izzy Muerte   22:33
Right.
That's that's partially a result of Python's dynamic execution and not not static typing.

Dave Abrahams   22:39
Yeah.
Yeah, it's like, you know, you have a an interactive interpreter, right?
And so when you hit a bug, you need to be able to get back to the prompt and they use exceptions.
To do that, you know if it were me, I would prefer that there was some parallel, but but different mechanisms so that I could so that I could keep the handling of those things separate.
But but I understand why they only have one.
OK, so.
Uh, next piece of advice.
Don't use exceptions for local failures right there.
There are optimized for the patterns of Handling.
Uh, problem.
Far from its source, so if you use them for local failures, that means you're gonna write a lot more catch blocks, which increases the complexity of code, right?
It's usually easy to tell what kind of whether a failure is local or not local, but I mean, just think about what the client a typical client is going to have to do.
But if you're writing a function and you really can't guess whether it's failure is going to be handled locally or not, maybe you should consider writing two functions, right?
One that that reports its failure using some other mechanism.
Umm.
And you know, one can call the other, so you don't need to reimplement it.
OK, next consider the performance implications of throwing.
So most languages actually aren't like this, but C implementations are usually biased really heavily towards optimizing the non failure case.
Umm, so that Handling of failure runs one or two orders of magnitude slower than code that's not Handling failure.
So, and that's tends to be a really great trade off because it allows them to skip explicit checks and all the branch prediction failures and other costs associated with checking for the error case on the hot path in the in the code, right.
And so this is what meant by zero cost exception handling.
Umm, if you've heard that term, uh and non local failures are rare in, you know, in terms of like the number of instructions executed and they don't happen repeatedly inside of tight loops, right?
But you know, if you're writing it, that also means if you're writing a tight loop, you know that's really on hot paths.
You don't want to repeatedly throw exceptions in there and and catch them.
If you're writing a real time system, for example, though, you might really want to think twice about using exceptions at all, because there's a.
It might be hard to predict the amount of slowdown that happens in those rare cases where an exception is actually thrown OK.
So I have an example that I think is God is useful so.
So I was one of the founding members of boost and and was involved in the design of the Boost Graph library and but when we were discussing that design, we realized that occasionally a particular use of a graph algorithm might wanna stop early.
Umm.
Now I guess to understand this.
Ohh well, I'll get to that.
OK, so for example Dijkstra's algorithm is.
That's an algorithm that finds all of the paths from A to B in order from shortest to longest, right?
So if you you give it two points in the graph, it'll tell you all of the the different ways to get from one to the other.
But suppose you want to find the 10 shortest paths and then stop.
Well, the way the the algorithms work, you pass them a visitor object that gets notified about results as they are discovered, right?
So they you can think of the algorithm as a loop that calls the visitor every time it finds a new path, for example.
And in fact, there are lots of notification points for various intermediate conditions, not just for finding the complete path.
Umm.
And so if we're going to handle this early stop thing explicitly, we need to generate an explicit test in the algorithm code after each of these points in the algorithms inner loop.
Right.
Uh.
So instead of doing that, which would both make the algorithm harder to read and uh and cost performance for branching, we decided to take advantage of C++'s bias toward optimizing the non failure case.
We set a visitor that wants to stop early.
Can just throw an exception right now.
To be perfectly fair, I don't think we ever benchmarked the effects of this choice, right?
So it might actually have been wrong from an optimization point of view in the end, but it was at least plausibly right, so there's nothing wrong with the with using an exception for that in principle.
If it actually gets you a performance win.
So finally you might also need to consider development culture and the way they the way your team uses their tools.
So some people typically set up their debuggers to stop whenever an exception occurs, and if you're in a team where that's an important practice, you might need to take some extra care not to throw when there's an alternate path to success, right?
Some developers get upset when code stops in a case that will eventually succeed.
OK, so enough about exceptions.
Umm.
So finally we come to the this is the good part.
This was originally gonna be the focus of the entire talk.
OK.
Umm, so I wanna talk about the obligations of the failing function and and of its caller.
So umm question is what do you put in the contract for a function that could fail and what does each side, the caller and the callee?
What do they need to do to ensure correctness?
So OK, the callee.
First of all, there's a documentation obligation you have to document any local failures and what they mean, because you're gonna report them as part of the as part of the return value, right? And.
Nonlocal failures you want to document at their source, right?
But not where they're just propagated from other functions that that they use.
So the problem is if you document them where they're propagated, you have the same problem as if you would included the types of the details of the failure in the type information right, which we talked about last time, creates a lot of churn as as failure reasons that don't really change anything about about the code end up changing.
Uh, as as you've all of your function implementations.
So.
OK so in code.
If you're the callee, if you have any unmanaged resources you've allocated, like you've opened a temporary file, you need to make sure that those things are are released.
Umm, the other example I I had is the the uninitialized memory that you're initializing right?
The the lifetime of those of those objects that you've put into that memory is a resource, and that needs to be.
They need to be, uh, denialist.
OK.
No, there's there's an optional thing that can be really useful if you're a mutating function.
So and and that is to consider saying that your transaction that if and that if there is a failure, the function has no effects.
Umm, that's often called the strong guarantee.
OK, now that can be a really useful guarantee to give when it falls out of the implementation, or at least a an efficient implementation.
Umm, but you don't want to do this if it adds performance cost.
So for example, the simplest way to give us a transactional guarantee on a function that mutates data is to do what I call copy and swap.
So first you make a copy of the data, you mutate the copy and place, and only when that succeeds, then you swap it back into place, right?
Swap it back to the original data and.
Sure, that ends up being transactional, but you pay the cost of making a full copy of the data and you don't wanna.
You don't want to preemptively do that?
Umm, because uh, what happens is often your caller doesn't need that.
That strong guarantee, right?
And what happens if all of the you know components get composed?
So what happens if all components do that copy and swap thing?
Now you have an exponential increase in cost, where at every level you're making copies.
It's sort of the same reason that we don't do object level locking, right.
Uh, you know, for umm concurrency logging, you know thread thread locking.
I saying this right you why we don't have a mutex in every object because.
Clients might need transactionality at a different level, right?
Might need your.
Your component might be a part of a bigger component and then you transactionality on that whole component.
So the locking of your individual component is a waste.
So to get the strong guarantee, sometimes you can do this just by reordering the operations you're performing.
For example, if you do all of the things that can fail before you actually make any mutations that are visible to clients, now you have the strong guarantee.
Umm uh so.
For you know, the simple example is, umm do all your memory allocations up front, then make changes that can't throw and and it's transactional.
So that's a useful thing to dock document when you can get it.
Right.
No, the caller umm.
So the caller's obligation is to discard any partially completed mutations to program state.
So if the caller is just calling a non mutating function right pinned and it throws, they don't have to do anything, they can just allow the the failure to propagate unless they happen to have some recovery strategy.
But I hope I already said this having a recovery strategy is really rare.
That usually means it's a nonlocal Error.
A nonlocal failure.
I mean, sorry, that usually means it's a local failure and the function shouldn't have been throwing in the 1st place so.
Umm.
So if you pass something to the function and and the function is gonna is gonna mutate that thing, you need to make sure that that thing gets gets discarded unless the function has given you this strong transactional guarantee.
Which case, it still has its original meaning, and it's and it's original value, right?
So when I say discard partial mutations to program state, umm, we have to talk about what counts as program state.
So that's data that can have an observable effect on the future behavior of your code.
So for example your if you have a log file that you're just streaming information into, that doesn't count as program state, right?
Because you never read it.
You never change, but the Programs behavior based on what's gone in there.
OK so.
So how do you arrange to discard partially mutated state?
Well, there's really only one strategy that really scales up in practice when mutations can fail.
Well, aside from the strategy of never mutating anything, but arguably that doesn't scale up either. Right?
Because then there's costs of copying.
So if you're, if you're not writing in a functional language, the pure functional language like Haskell, which most of us aren't, you have mutation.
Mutation can fail so.
So how do we manage discarding these partial mutations well?
Normally, the only strategy I've found that scales U is to propagate the responsibility for discarding this partial mutation.
All the way up to the top of the application and So what that means is.
You're at the top level.
Do you have to take this copy and swap strategy right?
You essentially you're gonna mutate a copy of the existing data and only replace the old copy when the mutation succeeds.
So but if you have a large data structure that could be really expensive, right?
To we we can't afford to copy an entire Photoshop document every time we make a change.
Well, actually we can, right?
And why?
Why is that the we do we actually do it?
And it's possible because Photoshop documents are essentially a persistent data structure.
You know, persistent, that's a confusing name because it doesn't have anything to do with persistence in the usual sense.
A persistent data structure is 1 where a partial mutation of a copy ends up sharing a lot of storage with the original.
So we store in Photoshop separate document for each state in the undo history.
But these copies share storage for any parts that weren't mutated between revisions, and this sharing behavior falls out naturally when you compose your data structure from copy on write parts.
So the original copy has basically 0 cost.
It's about, you know, bumping a reference count and then when you start to make changes, something is checking the reference count saying ohh if there's more than one reference.
Now I need to copy that part of the data that's changing.
So everybody follow that one, make sure I.
Yeah.
So there are some hints that's.
Let's hear from those.

Stephen DiVerdi   40:05
Hey.
Yeah.
Thanks Dave.
And and question and if this is harping on a previous topic then then let me know when we can just skip it.
But what I'm wondering is, it seems like what you just described about this mechanism for copying, mutating, and then replacing with the ability to handle local failures and robust to local failures also works for being robust to local errors.
And so I don't, I guess I still don't understand why that wouldn't be preferable to handle errors within that same framework of mutating a copy and then replacing it a transactional manner instead of crashing the application.

Dave Abrahams   40:45
Well.
This is.
Is a good question.
If you really have, if you really have data isolation and and you know that the only thing being mutated is this is this copy that will be discarded.
I think you might be safe.
To continue.
Uh, Sean?

Sean Parent   41:26
Yeah, I agree with that that the question is, do you really have data isolation?
And my answer would be, you know, in in C++, almost certainly not.
Ohm so.

Dave Abrahams   41:41
Yeah.

Sean Parent   41:41
Yeah.

Dave Abrahams   41:41
There, there, there's there's.
There's often, usually there's something that's being mutated that isn't the that isn't just the document state and and that that.
Whose?
Whose mutation isn't going to get undone by by discarding the partially mutated document state.
For example, you might have a queue of background operations, right?
Things get added to that queue.
Right.
And we don't have a we don't have a way to rollback that ad and some mutation fails.

Stephen DiVerdi   42:30
OK. Thanks.

Dave Abrahams   42:38
I guess I guess another another issue is like so part of the way we get this copy on write behavior with Photoshop is using the VM system with the you know which is.
A bunch of copy on write tiles essentially.
So if a bug were detected in that.
That would that would undermine the guarantees of the that you get from having copy on, right?
Right.
So the the the real problem with with bugs is you can't count on the systems that that uh normally give you this.
This their recovery property.
Uh, David sankel.

David Sankel   43:29
Yeah, I was just going to say that, you know, if if a bug is detected.
You all you know is that a bug is.
Detective, you have.
You have no idea of what the nature of the bug is.
I mean it could be corrupted memory, so even if you try to take your you know copy on write Das structure and discard it, it could be the old thing got messed up somehow because of some random thing.
You really, if you're really know nothing about the nature of a bug when it happened.
So the idea of recovering from it is.
Umm, it's not really sound I think.

Dave Abrahams   44:07
Yeah.
So I mean I have to like we have to think about, we have to think about the the nature of the environment in which we're running, so.
So I if if I think about you know how this would how this would play out in Hilo or in Rust?
Umm, you know, provided the bug didn't occur in unsafe code which has to be very carefully vetted.
Then you really know what stuff you're you're you're mutating.
When you do a mutation right and so you've really wouldn't know that the original state was was intact.
The problem with C++ is that.
We don't really have those kinds of protections and when there's a bug, it very typically leads to undefined behavior, which very typically could corrupt your old state, right?
It's undefined behavior and other words, it can do anything.
That's one of the you know, if you look at the C standard and and find all of the places where it says the behavior is undefined and you know there are lots of those and a lot of a lot of them apply in many, many places like there are statements like you know if any argument to a standard library function violates a precondition, the behavior is undefined.
Right.
And so that's the problem with with the C++ environment.
So it can really can undermine all of the guarantees that you would be getting from something like like copy on write system.
OK.
Umm.
Moving on.
Uh, I can't see if there are any more hands because I've got a window covering it, but I think there aren't good.
Umm OK so.
Yeah, some, some, some last advice.
Uh that I just added.
Uh.
About what to do when an assertion fires?
Umm.
And this is because especially what not to do because we see this a lot.
So first of all, don't remove the assertion, because the program seems to work when you take it out right the.
That's that's just the case you've tested.
Right.
And the what?
The assertion is saying.
Usually it's usually a precondition check with the assertion is if it's a precondition check, the assertion is saying.
The the owner of the function is saying you did something for which I'm not guaranteeing any particular result.
I don't know what was what result you should expect to get under these conditions.
Right.
So just taking it out doesn't make the program work.
The there are probably some effects that you aren't able to observe that that put the program in a broken state.
Uh.
Another thing not to do is don't go to the owner of the assertion and complain that they're crashing the program.
Remember the an assertion is a controlled shutdown in response to a detected bug, right?
And the first thing you need to do is to understand what kind of check is being performed, right?
So if it's a precondition check in someone else's component, that's probably your bug.
You're probably calling that that component in the wrong way.
Another possibility is that it's a self check, right?
What people often called sanity check, although we we try not to use that term anymore these days.
Umm.
Or it's a post condition check.
Uh, and in those cases, you want to talk to the the owner of the code about why the assumptions might have been violated.
That is, is very possibly a bug in the code that you're using, but this just reminds us why it's important to have different kinds of assertion macros or functions that tell you what their purpose is so that when they fire, people know what to do about them.
Uh, and my last bit of advice is you probably don't wanna use assertions.
Umm, you know the same functions you use for checking preconditions for doing your unit tests.
One reason is people often uh.
So typically when a unit test failure occurs, you don't go ahead using the same data, right?
You typically throw it out and go on to another test, and the other test you know uses fresh data and so that hasn't invalidated the rest of your testing.
People would like to hear about all of the test failures rather than just the just the first one.
So the assertions that exit the program aren't really appropriate there.
You want a different suite for doing those kind of checks, and that's all I've got for you.
Ready to open the floor to questions.

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
