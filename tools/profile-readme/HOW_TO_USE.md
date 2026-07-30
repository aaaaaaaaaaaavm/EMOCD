# Publishing the profile README

GitHub shows the README of a repository **named exactly after the account** at the top of the
profile page. It is the first thing a visitor sees after clicking through from a repository.

## One-time setup

1. Create a new **public** repository named exactly `aaaaaaaaaaaavm`.
   GitHub confirms when you have found the special repository name. If it does not, the
   name is wrong.
2. Copy `README.md` from this directory into it and push.

```bash
gh repo create aaaaaaaaaaaavm --public --description "Profile"
git clone https://github.com/aaaaaaaaaaaavm/aaaaaaaaaaaavm.git
cp <this-dir>/README.md aaaaaaaaaaaavm/
cd aaaaaaaaaaaavm && git add README.md
git commit -m "Profile" && git push
```

## Then pin the repositories

Profile, then **Customize your pins**, and select `VOLLEY`, `VOLLEY-paper`, `VOLLEY-thesis`, `VOLLEY-lab`.
Pinning is separate from the README and has to be done in the web UI. Without it the four
repositories sit below everything else on the account.

## Why this file lives here

It is kept in the flagship rather than in the profile repo so it stays with the rest of the
programme's tooling, next to `bootstrap_repos.sh` and `publish_releases.sh`. **This directory is
the source; the profile repo is a copy.** Edit here, then re-copy, the same
generated-not-maintained rule the companion repositories follow, for the same reason.

## Constraints it is written under

- **No hardware claim.** The repository's front page states that nothing has been built, fired or
  measured, and the profile has to agree with it. This changes the day `B-1` produces a number.
- **No skill-percentage bars, trophy widgets or streak counters.**
- **The paper is described as a manuscript**, because it is written and unsubmitted.
