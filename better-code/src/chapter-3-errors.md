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

We'll divide errors into two categories:

> - **Bug**: code contains an avoidable[^avoidable] mistake. For
>    example, an `if` statement might test the logical inverse of the
>    correct condition.
>
> - **Failure**: a function could not fulfill its postconditions even
>   though its preconditions were satisfied.  For example, writing a
>   file might fail because the filesystem is full.

[^avoidable]: Although “bugs” are inevitable, every *specific* bug is
    avoidable.

## Recovery

The idea of recovery from errors may have started in the domain of compilers.

OK, So what do we mean by recovery?
So when I asked the web which I E do a lot, most of the hits define error recovery in terms of what a parser does when it hits a syntax error in your code and that kind of surprised me because it's it's kind of an esoteric but thing.
But, but yeah, it's a well established, uh idea in in compiler engineering.
So let's say that you left out a semicolon.
Umm, so this is just some C code, right?
Uh, the parts are could just stop right there, right here.
And if she one diagnostic about the missing symbol?
Uh, if that's the only possibility in that syntactic position, otherwise it might, it might have a less useful diagnostic, but most programming languages, the they're they don't do that, even though I often I wish they would.
They wanna give me all of the potentially useful diagnostics about errors and the rest of my code, and so you know, if the parser just starts, our starts over as though as though this is the beginning of the document, you know this is the whole document and discards its state.
Umm, you know, I'm going to get a lot of bogus error messages.
That's a pretty poor recovery because although the program continues, it's doing something that almost certainly doesn't make any sense.
So you know, it thinks F is a type.
Name it thinks X is a type name.
It's complaining about a type specifier.
It's and then there's this extra closing brace that doesn't match anything right where, whereas it was there.
So instead of doing that, parsers typically try to recover by pretending I had written something correct.
In this case, it just injects a phantom semicolon and continues so as a first cut and here that's why you end up with this with this second error that that makes a little bit more sense, right?
That call to, to F would be at least syntactically legal.
If I'd put the the close paren.
Earlier, OK.
So.
Umm OK so so as a first cut, let's say the covery is continuing to execute doing sensible work, right?
And but I really like a quote I found in a stack overflow answer.
I mean, well, we're still not, we're still not getting down to it.
Very technical definition.
I think this really captures the spirit, they said.
It's to Sally forth entirely unscathed, as those such an inconvenient event had never occurred in the 1st place.
And So what do they mean by unscathed?
Well, they mean that the program state is intact.
Not only are the invariants) upheld, umm, but the state makes sense given the inputs the program has received.
So in like that parsing case, if you start over, you know from the beginning after the error, then the state doesn't really make sense given the inputs.
It doesn't correspond to what you've already seen.
Umm, so here's another example.
If we have an error while we're applying a blur to some image, it's not enough that the users document is still a well formed file, right?
It also can't have some random or half finished changes that they didn't request.
So that's that would be that would be very scathed, OK.
OK, so let's talk about recovering from a bug.
So what would that mean?
Well, first it is sumes that you had some way to detect the bug, right?
And not all bugs are detectable, but let's assume that this one is.
So an example of a nondetectable bug is you are trying to sort something, but you're but you're comparison function returns random results.
So, so that doesn't satisfy the requirements for the the sorting function.
It's a precondition that that there's no way to actually check for.
OK.
Uh, so, uh.
So let's assume that we have a detectable bug, and usually that means some somebody's checking a precondition and that precondition check fails.
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
