# Voice samples: Rodney's real sentences

These are taken from his posts with his typos kept, picked for the parts that sound most like him. The only edit: em dashes became commas, because the skill bans them. Some of his older posts contain AI-polished passages ("game-changer", "seamlessly", "It's not just X; it's Y"). Those are deliberately left out, so don't copy them even if you find them in `_posts/`.

Each section is one post. Copy the moves, not the sentences.

## 2025-07-26-Web-Pentesters-cannot-do-CTFs-hold-my-shell.md
What's good everyone!

So, something a little different happened recently. I decided to dive head-first into the Cybercon CTF challenge for KNUST. Now, most of you know me as a web application penetration tester. My day-to-day is hunting for XSS, SQLi, and messing with business logic. I barely touch CTFs, but I figured, why not?

Long story short, I walked out with 2nd place and some Cybercon swag.

It got me thinking. The core skill set we use in penetration testing,that deep-seated need for problem identification is 100% applicable to CTFs.

This is where my own tool came in clutch.

And let me be clear, this stuff is very technical you must know what you're doing to understand the guidance. It's not a magic button.

It paved the way to get initial access on one of the endpoints through SSH using a private signed key. lol.

It was like having a master strategist whispering in my ear. "Try this first. If that fails, pivot to this. If that's a dead end, here's your third option." It would've taken me a while of searching to figure that out on my own.

Unfortunately, I came in 2nd. Next time, I'll go harder. ... But it also highlighted a weakness: the commands and the traditional CTF approaches. The muscle memory just wasn't there.

So, I guess I have to finally finish those beginner boxes in Hack The Box and officially add CTF practice to my learning process, alongside my labs.

This article was short, but the lesson was huge.

* **Bug Fix:** Squashed a nasty error that was spamming my Firebase server with a ton of POST requests. Things should be much smoother now.

I use Obsidian a lot, so I know where I want the Hunter's Board to go aesthetically and functionally. It'll just take time to build it out.

kuwguap out.
catch yall inna bit.
cheers.

## 2025-07-05-My-App's-Wildest-Week.md
Hey everyone, Kuwguap here.

Guess what? I have exams in two days. Yes, actual university exams. And what am I thinking about 24/7? RAWPA. My passion project has completely hijacked my brain, and I wouldn't have it any other way.

So, while I should be memorizing lecture notes, I thought I'd get you up to speed on the wild ride of the last few weeks.

Anyway, let's dive into the mistakes and the madness.

I'll start with the rookie mistake that came back to bite me. I had never done any real UI/UX design before this project. I watched a couple of YouTube videos, got inspired by the clean look of Whimsical (the tool I used for wireframing), and just started… drawing.

No device responsiveness. No specific screen sizes. Just rectangles on a screen. It looked good on my development PC, so I figured, "Ship it!" A few weeks ago, a tester rightfully pointed out that the mobile view was completely broken. I spent two full days untangling that mess and making the app truly responsive. Lesson learned: think about all screens from day one.

That aside… about two days ago, I noticed features on RAWPA were failing.

I had hit **16,000 reads and 20,000 writes** in a single day. That's the entire free quota on Firebase. With just 33 users, this was insane. I was dumbfounded. I could either wait a day for the quota to reset or I could put on my detective hat and debug.

The culprit? A series of logical bugs born from late-night coding sessions.

It was a dumb, brute-force way to solve a problem, and it was hammering the database.

Why? Because I was sleepy and not thinking straight.

Guess what? I did it anyway. I integrated **Upstash Redis**, added the environment variables, made a few tweaks, and boom, the speed improved dramatically. Sometimes I wish I'd started with Next.js, but after a failed attempt to migrate, I'm sticking with my React + Vite setup and making it work.

I had 79 subdomains to check. Instead of using an automated tool like Eyewitness, I went through them manually (I know, I like the hassle).

I found interesting endpoints and potential vulnerabilities, but I had no organized way to track them without losing my main train of thought. Then it hit me.

Introducing the **Hunter's Board**.

I found an unfiltered search parameter on one endpoint, a bypass of the main UTF-8 filter, and immediately created a card for it, adding the link and my notes. It just… clicked.

Did I mention I have exams in two days? Ugh. I'll try to post a couple more updates before I go dark for studying.

The brain is just getting started.

## 2025-11-16-Did-Evolution-Skip-Student-Hostels.md
Hey there! If you read one of my previous posts, "So What Now?", you know I've been wrestling with a particular absurdity for a while.

Picture this: We live in the 21st century. We can summon a private car with a finger tap, track a pizza delivery, and book a flight to Durban using three different apps. But when it comes to booking a student hostel in Ghana?

> did evolution skip student booking in ghana?

Seriously. You have platforms for booking anything from a cruise ship to a trotro...

> why do students have to walk around in search of hostels. are the resources not enough to curb this? is there even a problem here?

These are the questions I pondered for about a second, right before a thought hit me like a literal bag of bricks (maybe those bricks were meant for an unverified hostel, who knows?).

First, I had to avoid the cringe.
> I wasn't going for a name filled with buzz words like hostel something or book that thing. something unique and oddly satisfying.

Say hello to **Katalyma** (it's Greek for accommodation, and yes, it sounds way cooler than "HostelBooker Pro Max").

It took a whole year! a whole bunch of supabase RLS violations, CSS nightmares because I usually focus on the PC view and not mobile(terrible thing to do), and existential dread...to make this a reality. It wasn't just me, though; advice from some really woke people (you know who you are) pushed it in the right direction, especially when we figured out the tricky revenue model.

**After cooking in private, I'm here, and the sauce is ready to be served! Hot!!! Katalyma is now officially in beta.**

(like figuring out how to implement group booking, still dealing with this)

Let's make walking around in search of a hostel a bad memory.

Connect with me and let's talk tech, hostels, or just life:

## 2025-06-21-series-2-implementing-the-WPA-in-rawpa-part-2.md
What's up, everyone? I'm back with Part 2 on implementing the Web Penetration Assistant (WPA) logic in RAWPA.

I'll be real with you, though. It needs a lot of improvement. I had this super clear picture of how it would function in my mind, but somewhere along the way, I completely lost my train of thought, lol. It happens, right? Still, it's a solid foundation to build on.

Now for the exciting part: we're officially moving into the testing stage!

The main AI using RAG is still a bit off, lol, but don't hesitate, I'll get that sorted out soon.

We now have our first 11 users willing to test RAWPA and be early access users! It might seem like a small number to some, but if RAWPA helps even just one of them, I know I've done something great.

It took me a solid hour of battling with build issues, but we made it, and it's up and running.

In case you're reading this and feeling a little FOMO, don't worry!

That's all the updates for now. Thanks for following the journey.

And I'm out ✌️

## 2025-06-18-series-2-implementing-wpa-in-rawpa-part-1.md
Hey everyone, it's been a minute!

After laying down the initial groundwork and figuring out "so, what now?", I've been deep in the trenches turning the concept into a functional tool.

I'm happy to say that the project is, for the most part, "basically done."

The first output was fantastic! It worked. But as I tried to make the RAG model more precise, I ran into some noise in the responses, and eventually, the code broke.

RAWPA isn't just another "get bugs quick scheme." It's about hitting a roadblock where you're like, "damn, I've tried everything... so what now?" That's where RAWPA is there to help.

On my journey scouring the net, I realized **lostsec** has a site with almost the same purpose as what I'm building. Far from being discouraged, this gave me the will to continue.

I know some people might have the wrong idea about what this app is for, but I believe it will help someone out there, and that is good enough for me.

I'm scouring the deepest parts of the web, watching countless YouTube videos, and yes, spamming my LinkedIn connections for valuable information (I highly do not advise this, lol).

That's where I am so far. It's a grind.

I'm always open to suggestions, critics and improvements.

Anyone also willing to add a methodology can reach out(Methodologies are featured and credited once proven to have confidence)

Till next time

## 2025-06-23-series-3-Internet-meet-RAWPA-part-1.md
Hey internet, this is RAWPA, RAWPA internet!

Man, the journey of building RAWPA has been a rollercoaster of code, coffee, and some seriously insightful conversations.

You know I'm all about getting this tool into your hands for testing, so when inspiration strikes, I gotta act fast.

And act fast, I did. Check out what's new:

You're seeing that right! ... One of my connections dropped this gem of an idea, and I just had to make it happen. Huge shoutout to you for the contribution.

Adding LOLBAS, for instance, was pretty simple since they have an awesome API page specifically for this kind of integration. The other two, however, were a bit of a hassle. I had to download the files directly from their GitHub repos and parse them into my database. Thankfully, they were all in markdown, so grepping the data I needed was easy work.

But wait, there's more!

If you've got a methodology, a toolkit, or any ideas you think would level up RAWPA, hit me up!

I'm hyped about where this is headed, and I'll keep you all in the loop.

Stay tuned, and keep hacking 🥷🏾!

## 2025-06-25-series-3-internet-meet-RAWPA-part-2.md
Hey internet, you're not going to believe this. **RAWPA gained a brain.**

I've hardly been sleeping, pushing code and chasing ideas. Yesterday, I finally crashed for about six solid hours, and guess what? The idea for the new Pathway Methodology hit me like a bag of bricks. LOL.

And for those wondering, this isn't that initial AI idea I had. I lost that train of thought a while back, and trust me, it ain't coming back, guys. This is something new. Something better.

So, let's get into it. All developments start out as bare sculptures. Even with a complex backend, they're just... static. They don't learn.

Before you ask, yes, RAWPA also has a more general AI feature that was going to use a RAG model to help with user prompts. I won't bore y'all with the technicals (at least not for now), but getting the RAG model incorporated was a hassle.

I'm glad you asked.

## 2025-07-01-series-4-My-Pentesting-AI-Learned-A-New-Word-Orchestrate.md
Hey everyone, Kuwguap here.

It's been a minute(literally just a day or two lol) since we last talked about the journey with RAWPA. ... Gained 30 users and about 30% of them active daily.

I kept coming back to one word: **Orchestrate**.

That's it. That's the next step.

Now, for the classic developer reality check. The Pentest Orchestrator is fully functional and works flawlessly on my local development server.

So, while the feature is *built*, it's not yet *live*.

The journey continues, and I can't wait to get the Orchestrator into your hands. Stay tuned.

## 2025-05-09-so-what-now.md
Well, here we go. Putting thoughts down "on paper" – or rather, onto a digital page that anyone with an internet connection can stumble upon. It feels a little… exposed, to be honest.

Sometimes, you find yourself staring at a list of open services, thinking, "Okay… so what now?"

I can't divulge too much just yet – think of it as a recipe I'm still perfecting in the kitchen.

This isn't about automating everything. Far from it.

And I'm excited (and a little nervous) to share that journey with you. Stay tuned for the next installment.

## 2025-05-09-wireframing-ui-development.md
My first step was wireframing. I initially started with Balsamiq, thinking its simplicity would be a good fit. However, it quickly felt *too* simple for what I had in mind.

With the flow mapped out, it was time to tackle the UI in Figma. Let me tell you, it's a lot! I have a mental image of what I want, but translating that into a functional and visually appealing UI is proving to be a challenge.

Thankfully, YouTube is a lifesaver.

This is what the UI is now.

## 2025-06-18-blossom-hackathon.md
Hey everyone,

I'm excited to share a project I've been pouring my energy into lately: **Blossom**, a voice-enabled mental health companion. And guess what? I recently submitted Blossom to its very first hackathon!

Scope management was another big one – I had so many ideas for Blossom, but I had to prioritize the core features to deliver a functional prototype.

I've put together a short video showcasing Blossom in action. Take a look!
