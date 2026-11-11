# Dialog NG

KDE's file dialog — the one every KDE app opens to pick or save a file, and that Firefox, Chrome and
Flatpak apps get through the desktop portal — with:

- **quick filters by kind of file**: All files, Image, Document, Spreadsheet, Archive, Audio, Video,
  Code and data, as a row of chips above the files and as a section under the places; choosing a kind
  shows only those files, without the folders;
- **a roomier places sidebar**: icons never below 22 px, taller rows.

The labels come from KDE's own translations (KFileMetaData's file categories, KIO's "All Files"), so they
follow the language of the desktop.

Part of the NG desktop, with [Dolphin NG](https://github.com/Morzilla/dolphin-ng),
[Breeze NG](https://github.com/Morzilla/breeze-ng) and [NeoLine](https://github.com/Morzilla/neoline-icons).
The Breeze NG installer can install it too (part `dialog`).

## How it works

Only one library is replaced, `libKF6KIOFileWidgets`. `dialog-ng build` downloads KIO from invent.kde.org
**at the version installed on your system**, applies `dialog-ng.patch`, builds that library alone and puts it
in `~/.local/dialog-ng`. `dialog-ng on` makes the session load it (through `LD_LIBRARY_PATH`, from a
`~/.config/plasma-workspace/env` file) **only while its version matches the system's**: after an update of
KDE Frameworks the stock dialog comes back by itself until you run `dialog-ng build` again.
Nothing outside your home folder is touched.

## Install

    git clone https://github.com/Morzilla/dialog-ng.git
    cd dialog-ng
    ./dialog-ng deps     # KIO's build dependencies (sudo; dnf, apt or pacman)
    ./dialog-ng build    # a few minutes
    ./dialog-ng on       # then log out and in

Try it first in a single app: `./dialog-ng run kwrite`. Back to the stock dialog: `./dialog-ng off`
(from the next login). `./dialog-ng status` shows the built and the system versions.

## Licence

`dialog-ng.patch` changes KIO and is under KIO's licence, LGPL-2.0-or-later. The `dialog-ng` script is MIT.
Made by Morzilla with Claude (Anthropic), on top of KDE software.
