#!/usr/bin/env python3
"""Score a draft against Rodney's (kuwguap) writing and scan it for AI tells.

Usage:
  style_check.py DRAFT.md                  # score against references/profile.json
  style_check.py DRAFT.md --json           # machine-readable output
  style_check.py --build-profile [POSTS_DIR] [--exclude NAME]   # rebuild profile
  style_check.py --loo [POSTS_DIR]         # leave-one-out calibration on real posts

Similarity (0-100) = 60% stylometry (sentence rhythm, tense mix, pronouns,
punctuation, idiolect) + 40% function-word fingerprint (Burrows' Delta).
A feature inside the author's own one-SD range gets full credit.
"""
import json, math, os, re, sys, glob, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(HERE, '..', 'references', 'profile.json')
DEFAULT_POSTS = os.path.join(HERE, '..', '..', '..', '..', '_posts')

# ---------- text cleaning ----------
def clean(md):
    md = re.sub(r'\A---\n.*?\n---\n', '', md, flags=re.S)          # front matter
    md = re.sub(r'```.*?```', '', md, flags=re.S)                  # code blocks
    md = re.sub(r'<[^>]+>', '', md)                                # html
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)                   # images
    md = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', md)               # links -> text
    md = re.sub(r'https?://\S+', '', md)
    md = re.sub(r'`[^`]*`', 'X', md)                               # inline code
    return md

def paragraphs(md):
    out = []
    for p in re.split(r'\n\s*\n', md):
        p = p.strip()
        if not p or re.match(r'^#{1,6} ', p):
            continue
        lines = [re.sub(r'^\s*(?:[*+-]|\d+\.)\s+', '', l) for l in p.split('\n')]
        lines = [re.sub(r'^>\s?', '', l) for l in lines]
        out.append(' '.join(lines))
    return out

def strip_md(s):
    return re.sub(r'[*_#>]', '', s)

def sentences(text):
    text = strip_md(text)
    parts = re.split(r'(?<=[.!?])\s+(?=["“(]?[A-Za-z0-9])|\n+', text)
    return [s.strip() for s in parts if len(re.findall(r"[A-Za-z']+", s)) >= 1]

WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
def words(text):
    return [w.lower().replace('’', "'") for w in WORD.findall(strip_md(text))]

# ---------- lexicons ----------
IRREG_PAST = set('was were had did got went made came saw thought found took gave told felt knew left put kept began built sent spent ran wrote brought caught hit set lost quit sat stood understood became drew fell held led meant paid read said slept woke won broke chose forgot shot struck threw tried decided realized started wanted needed noticed figured pushed moved'.split())
PRESENT = set("is are am has do does 's 're 'm".split())
FP_SING = set("i me my mine myself i'm i've i'll i'd".split())
FP_PLUR = set("we us our ours we're we've we'll".split())
SECOND = set("you your yours you're you've you'll y'all yall".split())
IDIOLECT = [r'\blol\b', r'\bguess what\b', r'\bstay tuned\b', r'\bhyped\b', r'\bclutch\b',
            r'\btrain of thought\b', r'\bthought train\b', r'\bbag of bricks\b', r"\by'?all\b",
            r'\bman,', r'\bhonestly\b', r"\bi'?ll be real\b", r'\bhit me up\b', r'\bshoutout\b',
            r'\bsauce\b', r'\bcooking\b', r'\bdumb\b', r'\binsane\b', r'\bgrind\b', r'\bugh\b',
            r'\bseriously\b', r'\bwhat\'?s (?:up|good)\b', r'\bkuwguap\b', r'\bout\.', r'\bbasically\b',
            r'\bi gotta\b', r"\bain'?t\b", r'\bboom\b', r'\bbeast\b', r'\bhassle\b', r'\bmadness\b',
            r'\bchaos\b', r'\bcatch (?:y\'?all|yall)\b', r'\bcheers\b', r'\bkeep hacking\b']
CONTRACTION = re.compile(r"\b\w+'(?:s|re|m|ve|ll|d|t)\b|\bain't\b|\by'all\b")

# ---------- features ----------
def feats(md):
    body = clean(md)
    paras = paragraphs(body)
    text = '\n'.join(paras)
    sents = [s for p in paras for s in sentences(p)]
    ws = words(text)
    n = max(len(ws), 1); per100 = 100.0 / n; per1k = 1000.0 / n
    slen = [len(words(s)) for s in sents] or [0]
    past = sum(1 for w in ws if w in IRREG_PAST or (w.endswith('ed') and len(w) > 4))
    pres = sum(1 for w in ws if w in PRESENT) + len(re.findall(r"\b(?:it|that|there|what|he|she)'s\b", text.lower()))
    low = text.lower().replace('’', "'")
    heads = len(re.findall(r'^#{2,6} ', body, flags=re.M))
    bullets = len(re.findall(r'^\s*(?:[*+-]|\d+\.)\s+', body, flags=re.M))
    f = {
        'sent_len_mean': st.mean(slen),
        'sent_len_sd': st.pstdev(slen),
        'short_sent_ratio': sum(1 for x in slen if x <= 6) / len(slen),
        'long_sent_ratio': sum(1 for x in slen if x >= 30) / len(slen),
        'word_len_mean': st.mean(len(w) for w in ws) if ws else 0,
        'sents_per_para': len(sents) / max(len(paras), 1),
        'first_person_sing': sum(w in FP_SING for w in ws) * per100,
        'first_person_plur': sum(w in FP_PLUR for w in ws) * per100,
        'second_person': sum(w in SECOND for w in ws) * per100,
        'contractions': len(CONTRACTION.findall(low)) * per100,
        'question_ratio': sum(s.rstrip().endswith('?') for s in sents) / max(len(sents), 1),
        'exclaim_ratio': sum(s.rstrip().endswith('!') for s in sents) / max(len(sents), 1),
        'parens': text.count('(') * per1k,
        'ellipsis': (low.count('...') + low.count('…')) * per1k,
        'initial_conj': sum(bool(re.match(r"^(and|but|so|now|anyway|still|plus|yes|okay|ok)\b", s.lower())) for s in sents) / max(len(sents), 1),
        'past_ratio': past / max(past + pres, 1),
        'perfect_rate': len(re.findall(r"\b(?:i've|we've|has|have|it's) (?:been|got|had|made|done|finally|just|hardly|pretty)\b|\b(?:i've|we've)\b", low)) * per1k,
        'future_rate': len(re.findall(r"\b(?:i'll|we'll|will|gonna|going to|gotta)\b", low)) * per1k,
        'ly_adverbs': sum(1 for w in ws if w.endswith('ly') and len(w) > 4) * per100,
        'commas_per_sent': text.count(',') / max(len(sents), 1),
        'idiolect': sum(len(re.findall(p, low)) for p in IDIOLECT) * per1k,
        'headings_per_1k': heads * per1k,
        'bullets_per_1k': bullets * per1k,
        'mattr': mattr(ws),
    }
    return f, ws

def mattr(ws, win=100):
    if len(ws) <= win:
        return len(set(ws)) / max(len(ws), 1)
    vals = [len(set(ws[i:i + win])) / win for i in range(0, len(ws) - win + 1, 10)]
    return st.mean(vals)

# ---------- AI-tell scanner ----------
HARD_TELLS = [  # (regex, why)
    (r'—', 'em dash (the #1 AI tell; you type "..." or a comma instead)'),
    (r'\bdelv(?:e|es|ing)\b', '"delve"'), (r'\btapestry\b', '"tapestry"'), (r'\btestament to\b', '"a testament to"'),
    (r'\b(?:ever-evolving|fast-paced|ever-changing)\b', 'stock AI adjective'),
    (r'\bseamless(?:ly)?\b', '"seamless(ly)"'), (r'\bcutting-edge\b', '"cutting-edge"'),
    (r'\bgame[- ]chang(?:er|ing)\b', '"game-changer"'), (r'\bleverag(?:e|es|ing)\b', '"leverage"'),
    (r'\brobust\b', '"robust"'), (r'\bunlock(?:s|ing)? (?:the|your|new)\b', '"unlock the/your"'),
    (r'\b(?:empower|elevate|harness|foster|streamline)(?:s|d|ing)?\b', 'corporate AI verb'),
    (r'\b(?:realm|landscape|paradigm|synergy|holistic|multifaceted|intricate|pivotal|nuanced)\b', 'AI abstract noun/adjective'),
    (r'\bin today\'?s (?:digital |modern |fast)', '"in today\'s ... world"'),
    (r'\b(?:moreover|furthermore|additionally|consequently|nonetheless|notably|previously|ultimately|looking ahead)\b', 'formal transition word'),
    (r'\bin conclusion\b|\bin summary\b|\bto sum up\b|\boverall,', 'essay-style wrap-up'),
    (r"\bit'?s (?:important|worth) (?:to note|noting)\b", '"it\'s worth noting"'),
    (r"\b(?:it'?s|it is|this is|that'?s|that is|is) not (?:just|only|merely|about) [^.;!?]{1,60}[;,.]\s*(?:it'?s|it is|this is|that'?s|but)\b", '"it\'s not X, it\'s Y" construction'),
    (r"\bnot (?:just|only) [^.;!?]{1,40}, but (?:also )?\b", '"not just X, but Y"'),
    (r"\b(?:wasn'?t|isn'?t|was not|is not) (?:really )?(?:the |a |about )?[^.;!?]{1,40}[,;]\s*it (?:was|is|'s)\b", '"the problem wasn\'t X, it was Y" reveal'),
    (r"\byou know the (?:story|drill)\b|\bwe'?ve all been there\b", 'fake-intimacy line'),
    (r"\blike (?:it|they|he|she) owed me\b|\blike a (?:kid|child) (?:in|on) a\b", 'crafted simile (he is earnest, not clever)'),
    (r"\b(?:isn'?t|aren'?t) just (?:a|an|another) [^.;!?]{1,40}[.;,]\s*(?:it'?s|they'?re)\b", '"isn\'t just X. It\'s Y"'),
    (r"\blet'?s dive (?:in|into)\b|\bdive deep\b|\bdeep dive into the world\b", '"let\'s dive in"'),
    (r"\bhere'?s (?:the (?:thing|kicker|breakdown|catch|deal|truth|scoop)|how it works|what you need)\b", '"here\'s the thing/deal/breakdown"'),
    (r'\bnavigat(?:e|ing) the (?:complex|ever|world|challenges)', '"navigate the complex..."'),
    (r'\bthe best of both worlds\b', 'cliche'), (r'\bembark(?:ed|ing)? on\b', '"embark on"'),
    (r'\bwhether you\'?re a [^.]{1,40} or a\b', '"whether you\'re an X or a Y"'),
    (r'\bbuckle up\b|\bwithout further ado\b|\bstay curious\b|\bhappy (?:coding|hacking)\b', 'stock sign-off'),
    (r'\bactionable insights?\b|\bvaluable insights?\b|\bkey takeaways?\b', 'consultant-speak'),
    (r'\b(?:crucial|vital|essential) (?:role|to understand)\b|\bplays? a (?:crucial|key|pivotal|vital) role\b', '"plays a crucial role"'),
    (r'\bI hope this (?:post|article|helps)\b', '"I hope this helps"'),
    (r'\bdive into the\b.*\bworld of\b|\bthe world of\b', '"the world of X"'),
]
SOFT_TELLS = [  # fine once, suspicious when stacked
    (r'\bjourney\b', '"journey" (you use it, max 1 per post)', 1),
    (r'\bexcited\b', '"excited" (max 1)', 1),
    (r'\bincredibl[ey]\b', '"incredible/incredibly" (max 1)', 1),
    (r'\bamazing\b', '"amazing" (max 1)', 1),
    (r'\bcomprehensive\b', '"comprehensive" (max 0-1)', 1),
    (r'\binsight(?:s|ful)?\b', '"insight(ful)" (max 1)', 1),
    (r'\b(?:truly|genuinely|deeply)\b', 'intensifier (max 1)', 1),
    (r'\bthe magic happens\b|\bthe real magic\b', '"the magic" (max 1)', 1),
    (r'(?m)^\s*(?:[*-]) \*\*[^*]+:\*\*', 'bold-label bullet list "**Label:** text" (max 3 such bullets)', 3),
    (r':', 'colon-heavy explaining (max 1 per 120 words)', None),
]

def tells(md):
    body = clean(md)
    low = body.replace('’', "'")
    nwords = len(words(body))
    hard, soft = [], []
    for rx, why in HARD_TELLS:
        hits = re.findall(rx, low, flags=re.I)
        if hits:
            hard.append((why, len(hits)))
    for rx, why, cap in SOFT_TELLS:
        n = len(re.findall(rx, low, flags=re.I))
        if cap is None:
            cap = max(2, nwords // 120)
        if n > cap:
            soft.append((why, n, cap))
    # catchphrase stacking: signature phrases from SKILL.md used verbatim
    sig = [r"a whole different beast", r"i'?ll be real with you", r'\bman,', r'\bboom\b', r'\bguess what\b', r'\bthe culprit\?', r'\bthen it hit me\b',
           r'\bcame in clutch\b', r'\bbag of bricks\b', r'\bhyped\b', r'\bugh\b', r'\bseriously\.', r'\bkeep hacking\b']
    nsig = sum(1 for rx in sig if re.search(rx, low, flags=re.I))
    if nsig > 5:  # his busiest post (Wildest Week) uses 5
        hard.append(('catchphrase stacking: %d different signature phrases, max 5 (blind readers flag this)' % nsig, nsig))
    # rule-of-three stacks: "X, Y, and Z" adjective/noun triplets
    triples = len(re.findall(r'\b\w+, \w+(?: \w+)?,? (?:and|or) \w+', low))
    if triples > max(1, nwords // 350):
        soft.append(('rule-of-three lists "X, Y, and Z"', triples, max(1, nwords // 350)))
    # headings every few lines = listicle
    heads = len(re.findall(r'^#{2,6} ', body, flags=re.M))
    if nwords and heads * 1000 / nwords > 9:
        soft.append(('too many headings (listicle shape)', heads, int(9 * nwords / 1000)))
    # uniform sentence lengths
    sl = [len(words(s)) for p in paragraphs(body) for s in sentences(p)]
    if len(sl) > 8 and st.pstdev(sl) < 5.5:
        soft.append(('sentence lengths too uniform (sd %.1f)' % st.pstdev(sl), 1, 0))
    # perfectly tidy: no lowercase slips, no fragments, no asides
    if nwords > 250 and not re.search(r'\blol\b|\(|\.\.\.|…', low, flags=re.I):
        soft.append(('too polished: no "lol", parenthetical aside or "..." anywhere', 1, 0))
    return hard, soft

# ---------- profile + scoring ----------
def load_posts(d, exclude=None):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, '*.md'))):
        name = os.path.basename(p)
        if exclude and exclude in name:
            continue
        out[name] = open(p, encoding='utf-8').read()
    return out

def build_profile(posts):
    F = {k: feats(v)[0] for k, v in posts.items()}
    keys = list(next(iter(F.values())).keys())
    prof = {'features': {}, 'posts': list(posts)}
    for k in keys:
        vals = [F[p][k] for p in F]
        prof['features'][k] = {'mean': st.mean(vals), 'sd': max(st.pstdev(vals), 1e-6 + 0.05 * abs(st.mean(vals)))}
    # function-word fingerprint: top-80 words across the corpus
    allw = []
    for v in posts.values():
        allw += feats(v)[1]
    freq = {}
    for w in allw:
        freq[w] = freq.get(w, 0) + 1
    mfw = [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:80]]
    rel = {p: relfreq(feats(v)[1], mfw) for p, v in posts.items()}
    prof['mfw'] = mfw
    prof['mfw_stats'] = {w: {'mean': st.mean(rel[p][i] for p in rel),
                             'sd': max(st.pstdev(rel[p][i] for p in rel), 1e-4)} for i, w in enumerate(mfw)}
    return prof

def relfreq(ws, mfw):
    n = max(len(ws), 1)
    c = {}
    for w in ws:
        c[w] = c.get(w, 0) + 1
    return [c.get(w, 0) / n for w in mfw]

def score(md, prof):
    f, ws = feats(md)
    per = {}
    for k, s in prof['features'].items():
        z = (f[k] - s['mean']) / s['sd']
        per[k] = {'value': round(f[k], 3), 'you': round(s['mean'], 3), 'z': round(z, 2),
                  'sim': max(0.0, min(1.0, 1 - (abs(z) - 1) / 2))}
    stylo = st.mean(v['sim'] for v in per.values())
    rf = relfreq(ws, prof['mfw'])
    delta = st.mean(abs((rf[i] - prof['mfw_stats'][w]['mean']) / prof['mfw_stats'][w]['sd'])
                    for i, w in enumerate(prof['mfw']))
    fw = max(0.0, min(1.0, 1 - (delta - 0.6) / 1.4))  # delta 0.6 (typical self) -> 1.0, 2.0 -> 0
    total = 100 * (0.6 * stylo + 0.4 * fw)
    hard, soft = tells(md)
    return {'similarity': round(total, 1), 'stylometry': round(100 * stylo, 1),
            'function_words': round(100 * fw, 1), 'burrows_delta': round(delta, 3),
            'words': len(ws), 'features': per, 'hard_tells': hard, 'soft_tells': soft,
            'rhythm_distance': round(rhythm_dist(per), 2),
            'rhythm_off': rhythm_off(per),
            'pass': total >= 80 and not hard and len(soft) <= 1 and all(t[1] <= t[2] + 1 for t in soft) and not rhythm_off(per)}

CORE = ['sent_len_mean', 'short_sent_ratio', 'commas_per_sent', 'word_len_mean', 'contractions', 'past_ratio']
RHYTHM_MAX = 1.4  # his own posts, held out, score 0.47-1.35
def rhythm_dist(per):
    return st.mean(abs(per[k]['z']) for k in CORE)
def rhythm_off(per):
    return rhythm_dist(per) > RHYTHM_MAX

def report(r):
    print(f"SIMILARITY  {r['similarity']}%   (stylometry {r['stylometry']}%, function-words {r['function_words']}%, delta {r['burrows_delta']}, {r['words']} words)")
    off = sorted(r['features'].items(), key=lambda kv: -abs(kv[1]['z']))[:6]
    print('Furthest from your voice:')
    for k, v in off:
        if abs(v['z']) > 1:
            print(f"  {k:20s} draft {v['value']:<8} you {v['you']:<8} z={v['z']:+.1f}")
    print('HARD AI TELLS (must be zero):', 'none' if not r['hard_tells'] else '')
    for why, n in r['hard_tells']:
        print(f'  x{n}  {why}')
    print('SOFT TELLS (over limit):', 'none' if not r['soft_tells'] else '')
    for t in r['soft_tells']:
        print(f'  {t[1]} > {t[2]}  {t[0]}')
    print(f"CORE RHYTHM DISTANCE {r['rhythm_distance']} (must be <= {RHYTHM_MAX}; avg SDs from him on: {', '.join(CORE)})")
    print('RESULT:', 'PASS' if r['pass'] else 'REVISE')

def main(a):
    if '--build-profile' in a:
        d = next((x for x in a[a.index('--build-profile') + 1:] if not x.startswith('--')), DEFAULT_POSTS)
        ex = a[a.index('--exclude') + 1] if '--exclude' in a else None
        out = a[a.index('--out') + 1] if '--out' in a else PROFILE
        prof = build_profile(load_posts(d, ex))
        json.dump(prof, open(out, 'w'), indent=1)
        print(f'profile from {len(prof["posts"])} posts -> {out}')
        return
    if '--loo' in a:
        d = next((x for x in a[a.index('--loo') + 1:] if not x.startswith('--')), DEFAULT_POSTS)
        posts = load_posts(d)
        for name in posts:
            prof = build_profile({k: v for k, v in posts.items() if k != name})
            r = score(posts[name], prof)
            print(f"{r['similarity']:5.1f}%  hard={sum(n for _, n in r['hard_tells'])}  {name}")
        return
    prof_path = a[a.index('--profile') + 1] if '--profile' in a else PROFILE
    prof = json.load(open(prof_path))
    r = score(open(a[0], encoding='utf-8').read(), prof)
    if '--json' in a:
        print(json.dumps(r, indent=1))
    else:
        report(r)

if __name__ == '__main__':
    main(sys.argv[1:])
