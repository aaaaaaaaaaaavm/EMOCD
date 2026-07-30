# Publishing the profile README

GitHub shows the README of a repository **named exactly after your username** at the top of your
profile page. It is the first thing anyone sees after clicking your name, and it is currently empty.

## One-time setup

1. Create a new **public** repository named exactly `aaaaaaaaaaaavm`.
   GitHub will show a message confirming you have found the special repository name, if it does
   not, the name is wrong.
2. Copy `README.md` from this directory into it and push.

```bash
gh repo create aaaaaaaaaaaavm --public --description "Profile"
git clone https://github.com/aaaaaaaaaaaavm/aaaaaaaaaaaavm.git
cp <this-dir>/README.md aaaaaaaaaaaavm/
cd aaaaaaaaaaaavm && git add README.md
git commit -m "Profile" && git push
```

## Then pin the repositories

Profile to **Customize your pins** to select `VOLLEY`, `EMOCD-paper`, `EMOCD-thesis`, `EMOCD-lab`.
Pinning is separate from the README and has to be done in the web UI. Without it the four
repositories are buried under everything else you own.

## Why this file lives here

It is kept in the flagship rather than in the profile repo so it stays with the rest of the
programme's tooling, next to `bootstrap_repos.sh` and `publish_releases.sh`. **This directory is
the source; the profile repo is a copy.** Edit here, then re-copy, the same
generated-not-maintained rule the companion repositories follow, for the same reason.

## What it deliberately does not say

- **No "this becomes hardware this semester."** Your LinkedIn summary says it. It is a good line
  and it may well be true, but the repository's own front page says nothing has been built, fired
  or measured, so a profile claiming imminent hardware next to a repository saying TRL 2-3 reads
  as overreach to exactly the audience you want. Put it back the day `B-1` produces a number.
- **No skill-percentage bars, no trophy widgets, no streak counters.** They signal the opposite of
  what this programme is arguing about you.
- **No claim of a paper being published.** It is written and unsubmitted. The README says
  "manuscript", which is accurate.
