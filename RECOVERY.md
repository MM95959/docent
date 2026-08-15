# Docent / FrameSync Recovery Guide

This document describes how to recover the Docent installation after replacing
the Mac, losing the local installation, or otherwise rebuilding the system.

## 1. Source Code

Docent:

    https://github.com/MM95959/docent.git

FrameSync:

    https://github.com/MM95959/FrameSync.git

The normal production branch for both projects is:

    main

Known-good recovery tags established during development:

    Docent:    v1.5.0
    FrameSync: v1.5.0

If main is ever in doubt during recovery, these tags provide a stable fallback
point.

Recommended local locations:

    ~/Developer/docent
    ~/Developer/FrameSync

GitHub contains the application source code and Git history, but intentionally
does NOT contain private configuration or locally generated Docent data.

## 2. Important Files Not Stored in GitHub

Important local Docent files include:

    .env
    collections.json
    artwork_meta.json

These are intentionally excluded by .gitignore.

On the current installation they are included in Time Machine backups.

Restore these files into:

    ~/Developer/docent/

Do not commit .env, API keys, passwords, or other secrets to GitHub.

## 3. Files That Do Not Need Independent Backup

These can be recreated:

    .venv/
    __pycache__/
    .cache/

Do not rely on restoring the old Python virtual environment.

## 4. Samsung Frame Connection

The current installation does not appear to use a persistent .tv-token file.

After rebuilding Docent, the Samsung Frame may therefore require authorization
again. If the TV displays a connection/authorization prompt, approve Docent on
the TV.

The TV address and other local configuration should be recovered from .env.

## 5. Recreate the Docent Environment

Clone Docent:

    cd ~/Developer
    git clone https://github.com/MM95959/docent.git

Restore the local configuration files described above.

The repository contains:

    pyproject.toml
    requirements.txt
    uv.lock

These allow the Python environment and dependencies to be recreated.

Follow the current setup instructions in README.md if installation details have
changed since this recovery guide was written.

Start Docent with:

    cd ~/Developer/docent
    ./Docent.command

Then open:

    http://localhost:8000

## 6. Recover FrameSync

Clone FrameSync:

    cd ~/Developer
    git clone https://github.com/MM95959/FrameSync.git

In Lightroom Classic, add or verify the FrameSync plug-in using the
FrameSync.lrdevplugin directory in the repository.

Publish Services and Publish Collections are catalog-specific and may need to be
recreated or reconnected after restoring a Lightroom catalog.

## 7. Restore Docent State

Restore, when available:

    .env
    collections.json
    artwork_meta.json

Then start Docent and confirm that the expected collections appear.

If a newly created collection does not immediately appear in the Docent browser,
reload the Docent page.

## 8. Recovery Validation

Before performing a large publish, use a small Lightroom Publish Collection and
verify:

1. New photographs publish successfully to the Samsung Frame.
2. The corresponding Docent collection is created and has correct membership.
3. Removing a photograph in Lightroom and publishing removes it from the Frame.
4. Modifying and republishing a photograph updates it without unwanted duplicates.
5. Display on Frame still works.
6. Art Mode, slideshow rotation, and normal TV sleep behavior still work.

For Docent, verify:

    cd ~/Developer/docent
    git branch --show-current
    git status
    git log -1 --oneline --decorate

For FrameSync, verify:

    cd ~/Developer/FrameSync
    git branch --show-current
    git status
    git log -1 --oneline --decorate

Both production installations should normally be on main.

## 9. Current Backup Strategy

The intended protection model is:

    GitHub       -> source code, Git history, recovery documentation
    Time Machine -> .env and local Docent state/configuration
    Lightroom    -> authoritative source for photographs and publish workflow
    Samsung TV   -> display destination, not an authoritative backup

GitHub should never be used to store passwords, API keys, or other secrets.

## 10. Known Operational Notes

- Docent thumbnail fetching is designed to fail quietly rather than repeatedly
  hammer the Samsung Art API.
- Missing thumbnails may show "Tap to retry".
- Removing the photo currently displayed on the Frame may cause the TV to leave
  My Photos; this is considered a minor Samsung-side behavior, not data loss.
- If Docent-to-TV communication becomes unreliable, first confirm only one
  Docent server instance is running before rebooting the TV.
