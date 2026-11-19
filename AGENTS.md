# AGENTS.md

Guidance for coding agents (and people) working on Dialog NG.

## What this is

Dialog NG is KDE's file dialog (the Open/Save window of every KDE application, and of Firefox, Chrome and Flatpak
applications through the desktop portal) in the look of [Dolphin NG](https://github.com/Morzilla/dolphin-ng): drawn
rows, a strip of filters by kind of file, groups, pinned items, a quick preview, a glass sidebar. Only one library
changes, `libKF6KIOFileWidgets`, built from the KIO release the system has, with `dialog-ng.patch` applied. What the
user sees is described in `README.md`.

The development branch is `main`.

## Layout

```
dialog-ng.patch             the change to KIO's src/filewidgets (the whole of Dialog NG)
dialog-ng                   build, on, off, status, run (see its header)
packaging/dialog-ng.spec    the Fedora package (COPR morzilla/desktop-ng): one KIO release per Fedora version
screenshots/
```

The code is not in this repository as files: it is a patch on KIO. The parts it touches:

| File in KIO's src/filewidgets     | What Dialog NG does there                                           |
|-----------------------------------|---------------------------------------------------------------------|
| `kfilewidget.cpp`                 | the strip (filter chips, sorting, view, groups), the sidebar, glass |
| `kdiroperatordetailview.cpp/_p.h` | the drawn rows, groups, quick preview; `NgLook` (Aurora colours)    |
| `kfileplacesview.cpp`             | the places in the sidebar                                           |
| `kdirsortfilterproxymodel.cpp`    | sorting by date created, pinned items first                         |
| `kurlnavigatorbuttonbase.cpp`     | the breadcrumb buttons                                              |

## Working on it

1. Clone KIO at the release tag of the system, e.g. `git clone --branch v6.32.0 https://invent.kde.org/frameworks/kio.git`.
2. Apply the patch: `git apply dialog-ng.patch`. Build the one target: `cmake --build build --target KF6KIOFileWidgets`.
3. Edit there, then regenerate the patch from the same base:
   `git diff v6.32.0 -- src/filewidgets > /path/to/dialog-ng/dialog-ng.patch`.
4. The patch must apply to every KIO release the package is built for (see `packaging/dialog-ng.spec`): check with
   `patch -p1 --dry-run < dialog-ng.patch` on each.

`./dialog-ng build` does steps 1 and 2 for the installed KIO and installs into `~/.local/dialog-ng`;
`./dialog-ng run kwrite` starts one program with it. `DIALOG_NG_DEMO_QUICKVIEW=name` opens the quick preview of that
file without pointing at it (for screenshots).

## Conventions

- **Keep KIO recognisable.** Mark Dialog NG code with `kio-ng:` comments, change KIO's code only where needed and
  do not reformat what you do not change: the patch is carried to every new KIO release.
- **Comments say why**, in plain English sentences.
- **Strings the user sees** in NG code: `ngLabel(domain, context, "English", "Italiano")`, which takes KDE's own
  translation when the words exist in a KDE catalogue.
- **Colours come from the palette**; a nearly colourless accent stays neutral (see `NgLook`).
- **Same look as Dolphin NG.** When Dolphin NG's rows or sidebar change, the dialog follows: what is selected or on
  wears the accent with white or black text by its lightness, and the sidebar's selection and section titles should
  be pills painted by the dialog, not the style's own rectangle (Dolphin NG does so, to match with stock Breeze too).
- **Glass needs the compositor's blur.** Breeze NG sets the application property `_breeze_ng_bare_glass` a moment
  after start when KWin has no blur (it cannot be known earlier): glass the dialog lays itself must then be solid.
- Check dark and light schemes and Breeze NG's looks; report what you built and looked at.

## Commits and packages

- Commit on `main` with the regenerated patch. The subject says what changed for the user; the body says why.
- `packaging/dialog-ng.spec`: after pushing, set `commit` and `snapdate` (`YYYYMMDDHHMM`) and add a changelog line.
  Publishing packages and releases is the maintainer's decision: ask first.
- Keep secrets and personal details out of code, commits and logs.
