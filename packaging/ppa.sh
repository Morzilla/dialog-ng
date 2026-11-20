#!/bin/bash
# packaging/ppa.sh SERIES [binary|source] [PPA_REVISION]: a Debian package of Dialog NG for an Ubuntu release (resolute,
# stonking...): the KIO release of that Ubuntu (KIO=x.y.z, else the one installed here) from download.kde.org, with
# the patch of this checkout for it (packaging/kio-patches/kio-x.y.z.patch, else dialog-ng.patch). Run inside an Ubuntu
# container or machine of that release, with the build tools (devscripts, debhelper, equivs).
#   binary  builds the .deb here, after installing the build dependencies (to test the packaging)
#   source  builds the source package for Launchpad, unsigned: then sign the .dsc and .changes and upload
#           (ppa-upload.sh dialog-ng). DEBEMAIL: the address of the signing key (the changelog's)
set -euo pipefail
SERIES=${1:?series}; MODE=${2:-binary}; REV=${3:-1}
HERE="$(cd "$(dirname "$0")/.." && pwd)"
KIO=${KIO:-$(dpkg-query -W -f='${Version}' libkf6kiofilewidgets6 | sed 's/-.*//')}
COMMIT=$(git -C "$HERE" rev-parse HEAD); SHORT=${COMMIT:0:7}
DATE=$(git -C "$HERE" log -1 --format=%cd --date=format:%Y%m%d%H%M)
UPSTREAM="${KIO}+${DATE}git${SHORT}"
VERSION="${UPSTREAM}-0ppa${REV}~${SERIES}1"
PATCH="$HERE/packaging/kio-patches/kio-${KIO}.patch"
[ -f "$PATCH" ] || PATCH="$HERE/dialog-ng.patch"
WORK=${WORK:-$(mktemp -d)}
cd "$WORK"
curl -sSfL "https://download.kde.org/stable/frameworks/${KIO%.*}/kio-${KIO}.tar.xz" -o "dialog-ng_${UPSTREAM}.orig.tar.xz"
tar xf "dialog-ng_${UPSTREAM}.orig.tar.xz"
mv "kio-${KIO}" "dialog-ng-${UPSTREAM}"
cd "dialog-ng-${UPSTREAM}"
cp -r "$HERE/packaging/debian" debian # (the packaging of the checkout, committed or not)
mkdir -p debian/patches
cp "$PATCH" debian/patches/dialog-ng.patch
echo dialog-ng.patch > debian/patches/series
cat > debian/changelog <<EOT
dialog-ng (${VERSION}) ${SERIES}; urgency=medium

  * Snapshot ${SHORT} of Dialog NG (https://github.com/Morzilla/dialog-ng/commit/${COMMIT}) on KIO ${KIO}.

 -- ${DEBFULLNAME:-Morzilla} <${DEBEMAIL:-3956663+Morzilla@users.noreply.github.com}>  $(LC_ALL=C date -R)
EOT
if [ "$MODE" = source ]; then
    dpkg-buildpackage -S -sa -d -us -uc # (signed afterwards, where the key is)
else
    mk-build-deps -i -r $([ "$(id -u)" = 0 ] || echo "-s sudo") -t "apt-get -y --no-install-recommends" debian/control >/dev/null
    dpkg-buildpackage -b -us -uc -j"$(nproc)"
fi
echo "built in $WORK"
