---
title: "Series 2: Implementing the WPA in RAWPA - Part 1"
date: 2025-06-18
layout: post
category: RAWPA
series: Implementing the WPA in RAWPA
series_part: 1
tags: [rawpa, wpa, cybersecurity, devlog, ai, rag-model]
---

Hey everyone, it’s been a minute!

Welcome back to the devlog for RAWPA. After laying down the initial groundwork and figuring out "so, what now?", I've been deep in the trenches turning the concept into a functional tool. This next series of posts is all about the journey of implementing the Web Pentesting Assistant (WPA), and let me tell you, it's been a ride.

## A Glimpse into the Future

One of the coolest parts of building something in public is the feedback and engagement from the community. A while back, I received some incredible feature ideas from one of my LinkedIn connections. It was one of those moments that gets you incredibly hyped about the future potential of your project.

He suggested things like:

* **Gamification:** Badges or rewards for completing sections.
* **Tool Integrations:** Direct interactions with tools like Nmap or Burp Suite.
* **Exportable Reports:** Automatically generate a report from completed methodology steps.
* **Collaborative Mode:** Teams can share steps, leave notes, and track progress together.
* **Built-in Assistant:** Like a Copilot for each step offering hints, payload suggestions, or real-time examples.

Reading that list was both exciting and humbling. It painted a clear picture of what RAWPA could become.A truly comprehensive and interactive platform. A huge thank you to him for that spark!

## The Reality Check: Where RAWPA Is Today

So, with all those amazing ideas floating around, where am I with the project right now?

I’m happy to say that the project is, for the most part, "basically done." The main logic has been established, the core framework is solid, and I even built out a fully functional **admin panel**. From there, I can add new methodologies, see user interactions, and manage the application's content, which is a huge step forward for making RAWPA scalable.
![User-Dashboard](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/rawpa-dashboard1.png)

Naturally, I got really excited about the "Built-in Assistant" feature. I started implementing it, opting to use a **RAG (Retrieval-Augmented Generation) model** for the AI. My plan was to avoid the heavy lifting of fine-tuning a model from scratch (for now) and instead give a model access to a curated dataset to work from. The RAG would fetch the right data, parse a user's command, and use some tags from the ARD to get a response from a Hugging Face model.

The first output was fantastic! It worked. But as I tried to make the RAG model more precise, I ran into some noise in the responses, and eventually, the code broke. I quickly realized that building and refining this AI feature is an easy fix, but dialing it in perfectly is a whole project on its own.

So, I made a strategic decision: I turned off the AI feature in the admin panel for now. It’s on the back burner, ready to be picked up again, but I need to focus on the core methodologies first.

## The Philosophy of RAWPA (Utmost Importance)

Before I go any further, I need to state something with utmost importance about the philosophy behind this project.

I highly recommend the manual process of going through files, manually checking for business logic vulnerabilities, and playing with tools like Burp Suite. RAWPA isn't just another "get bugs quick scheme." It's not about automation. It's about hitting a roadblock where you're like, "damn, I've tried everything... so what now?" That's where RAWPA is there to help.
![Deep-Recon-methodology](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/rawpa-staright2.png)

On my journey scouring the net, I realized **lostsec** has a site with almost the same purpose as what I'm building. Far from being discouraged, this gave me the will to continue, knowing there's a real need for this kind of guided thinking.

RAWPA is designed to help with muscle memory. Once you know what to do and have internalized the methodologies, RAWPA will wait patiently until you need it again. I know some people might have the wrong idea about what this app is for, but I believe it will help someone out there, and that is good enough for me.

## My Current Phase: The Deep Dive

So, what phase am I in right now? I'm in the deep-dive research phase.

This is the part of the project that isn't about code, but about knowledge. I'm scouring the deepest parts of the web, watching countless YouTube videos, and yes, spamming my LinkedIn connections for valuable information (I highly do not advise this, lol).

Every piece of information I find, I test against several use cases. I'm looking to see how confident the information is. If it's a technique that isn't already part of a formal methodology, I try to refine it and structure it until it *becomes* one. This rigorous process of research and validation is what will form the backbone of RAWPA's intelligence.
![guided-methodology-for-IDOR](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/rawpa-guided.png)

That’s where I am so far. It's a grind, but it's the most critical step to ensure that the "WPA" in RAWPA is something you can truly rely on. Stay tuned for Part 2, where I'll share what this deep dive has uncovered.
I'm always open to suggestions, critics and improvements. 

Anyone also willing to add a methodology can reach out(Methodologies are featured and credited once proven to have confidence)

Till next time 