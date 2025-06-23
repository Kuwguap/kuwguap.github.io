---
title: "Series 3: Internet meet RAWPA - Part 1"
date: 2025-06-23
layout: post
category: RAWPA
series: Internet meet RAWPA
series_part: 1
tags: [rawpa, wpa, cybersecurity, devlog, ai, rag-model]
---

Hey internet, this is RAWPA, RAWPA internet!

Man, the journey of building RAWPA has been a rollercoaster of code, coffee, and some seriously insightful conversations. I recently had a chat with a fellow pentester that completely lit up the path forward for RAWPA's development. You know I'm all about getting this tool into your hands for testing, so when inspiration strikes, I gotta act fast.6

And act fast, I did. Check out what's new:

![New RAWPA Features](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/RAWPA-features.png)

### Triple Threat Integration

You're seeing that right! We've integrated **LOLBAS**, **WADCOMS**, and **GTFOBins** directly into RAWPA. One of my connections dropped this gem of an idea, and I just had to make it happen. Huge shoutout to you for the contribution – this is what the community is all about!

Getting them integrated was an adventure in itself. Adding LOLBAS, for instance, was pretty simple since they have an awesome API page specifically for this kind of integration. The other two, however, were a bit of a hassle. I had to download the files directly from their GitHub repos and parse them into my database. Thankfully, they were all in markdown, so grepping the data I needed was easy work. Now you can access all three of these powerful resources in one place!
![GTFOBins integration](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/GTFO.png)

### More Tools in the Arsenal

But wait, there's more! While I was at it, I also rolled in a few more handy toolkits to broaden RAWPA's scope. We now have a dedicated **Pentest Toolkit**, a **Reverse Shell Generator**, and an **OSINT Toolkit**. The goal is to make RAWPA a comprehensive hub for hierarchical methodologies, guided pathways, toolkits, and workflows.

### Community-Driven and Growing

This is a community-driven project, and I mean that. If you've got a methodology, a toolkit, or any ideas you think would level up RAWPA, hit me up! Or even better, try out the new **"Contribute"** feature on the landing page. I'm all about giving credit where it's due, so all contributors will be recognized for their genius.

The testing phase has been incredible so far. We've got about **22 users** on board, with roughly half of them consistently using RAWPA daily. My biggest satisfaction comes from knowing that RAWPA is making a real difference for at least one person out there.

I'm hyped about where this is headed, and I'll keep you all in the loop. The future is bright, and the pentesting train of thought is about to get a serious rejuvenation.

Stay tuned, and keep hacking 🥷🏾