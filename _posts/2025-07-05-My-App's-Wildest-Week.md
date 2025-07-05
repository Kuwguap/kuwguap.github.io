---
title: "Rookie Mistakes, Infinite Loops, and a New Feature: My App's Wildest Week"
date: 2025-07-05
layout: post
category: RAWPA
series: Rookie Mistakes, Infinite Loops, and a New Feature
series_part: 1
tags: [rawpa, wpa, cybersecurity, devlog, ai, rag-model,neural-network]
---


Hey everyone, Kuwguap here.

Guess what? I have exams in two days. Yes, actual university exams. And what am I thinking about 24/7? RAWPA. My passion project has completely hijacked my brain, and I wouldn't have it any other way.

So, while I should be memorizing lecture notes, I thought I’d get you up to speed on the wild ride of the last few weeks. Before I dive into the bugs and the new feature, I have to say—I honestly think the number one skill in any tech career is debugging. It’s not just about finding errors; it's about problem analysis, understanding, and solving. It's a superpower. It’s cool to create something new, but being able to fix what's broken—whether it's your own code or a target system—is where the real magic happens.

Anyway, let's dive into the mistakes and the madness.

### My First Mistake: The "Responsive What?" UI

I’ll start with the rookie mistake that came back to bite me. I had never done any real UI/UX design before this project. I watched a couple of YouTube videos, got inspired by the clean look of Whimsical (the tool I used for wireframing), and just started… drawing.
![RAWPA login vs Whimsical login](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/whim-raw.png)

No device responsiveness. No specific screen sizes. Just rectangles on a screen. It looked good on my development PC, so I figured, "Ship it!" A few weeks ago, a tester rightfully pointed out that the mobile view was completely broken. I spent two full days untangling that mess and making the app truly responsive. Lesson learned: think about all screens from day one.

### The Bug That Shut RAWPA Down

That aside… about two days ago, I noticed features on RAWPA were failing. The methodologies weren't loading, and other data was missing. A quick look at my console told the story:

`FirebaseError: [code=resource-exhausted]: Quota exceeded.`

I had hit **16,000 reads and 20,000 writes** in a single day. That's the entire free quota on Firebase. With just 33 users, this was insane. I was dumbfounded. I could either wait a day for the quota to reset or I could put on my detective hat and debug.
![Firestore quota reached](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/quota.png)

The culprit? A series of logical bugs born from late-night coding sessions.
1.  **The Infinite Loop:** I had created a function that continuously checked Firestore for updates, in case I used my admin panel to disable a methodology. It was a dumb, brute-force way to solve a problem, and it was hammering the database.
2.  **Sleepy-Dev Syndrome:** The new feature I was building needed to save its state. Instead of using `localStorage` for frequent, small updates, I was writing to Firestore on every single change. Why? Because I was sleepy and not thinking straight.

On top of that, the app was loading all Firestore functions on startup, creating a queue that led to insane load times—sometimes up to 10 seconds. I knew the fix was probably caching with something like Redis, but I was hesitant. It meant more complexity and moving things around on Vercel, which has a 12-API limit on the free plan.

Guess what? I did it anyway. I integrated **Upstash Redis**, added the environment variables, made a few tweaks, and boom—the speed improved dramatically. Sometimes I wish I’d started with Next.js, but after a failed attempt to migrate, I'm sticking with my React + Vite setup and making it work.
![Upstash console](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/upstash.png)

### The New Feature, Born from a Real Pentest

So, what was this new feature I was building that caused all the chaos?

It started while I was working on a target from HackerOne. I was using my other tool, AAweRT, for recon and realized my thought process has completely changed since building RAWPA. I had 79 subdomains to check. Instead of using an automated tool like Eyewitness, I went through them manually (I know, I like the hassle).

I found interesting endpoints and potential vulnerabilities, but I had no organized way to track them without losing my main train of thought. Then it hit me.

Introducing the **Hunter's Board**.

![Hunter's Board](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/hunterboard.png)

It’s a Kanban-styled board built directly into RAWPA, designed for the way a pentester thinks. You can create cards for anything: domains, methodologies, findings, reports, code snippets, tools, you name it.

As I was checking those 79 subdomains, I was developing this board. I found an unfiltered search parameter on one endpoint—a bypass of the main UTF-8 filter—and immediately created a card for it, adding the link and my notes. It just… clicked.

The Hunter's Board is now live on the site! You can check it out now.

As a quick update, I've temporarily removed the **RAWPA AI** and **Pentest Orchestrator** features. I need to optimize them and fix some backend issues before they're ready for prime time, and I want the user experience to be perfect.

Did I mention I have exams in two days? Ugh. I’ll try to post a couple more updates before I go dark for studying.

Until next time, remember that RAWPA is a community project. If you have ideas, feedback, or want to contribute, use the "Contribute" feature on the site or connect with me on [LinkedIn](https://www.linkedin.com/in/glenn-osioh-85104827b/). Check out the project at [https://rawpa.vercel.app/](https://rawpa.vercel.app/).

The brain is just getting started.