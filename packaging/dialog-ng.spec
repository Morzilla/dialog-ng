# SPDX-License-Identifier: MIT
%global commit      d26d2ccf146ad4401953b86dccf24e04109e7c80
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate    202611161152
# built from the KIO release each Fedora ships: the patched library must match the installed one
%if 0%{?fedora} >= 45
%global kio         6.32.0
%global kiosource   2
%else
%global kio         6.31.0
%global kiosource   0
%endif
%global ngprefix    /opt/ng/dialog-ng

Name:           dialog-ng
Version:        %{kio}^%{snapdate}git%{shortcommit}
Release:        1%{?dist}
Summary:        KDE's file dialog with quick filters and Dolphin NG's look
# the library is KIO's, patched: KIO's licences; the packaging is MIT
License:        LGPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-only AND LGPL-2.1-only AND LGPL-3.0-only AND (LGPL-2.1-only OR LGPL-3.0-only) AND GPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND MIT
URL:            https://github.com/Morzilla/dialog-ng
Source0:        https://download.kde.org/stable/frameworks/6.31/kio-6.31.0.tar.xz
Source1:        https://raw.githubusercontent.com/Morzilla/dialog-ng/%{commit}/dialog-ng.patch
Source2:        https://download.kde.org/stable/frameworks/6.32/kio-6.32.0.tar.xz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= %{kio}
BuildRequires:  gcc-c++
BuildRequires:  kf6-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6UiPlugin)
BuildRequires:  cmake(KF6Archive)
BuildRequires:  cmake(KF6Bookmarks)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Completion)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6DocTools)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IconThemes)
BuildRequires:  cmake(KF6ItemViews)
BuildRequires:  cmake(KF6JobWidgets)
BuildRequires:  cmake(KF6KDED)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6Solid)
BuildRequires:  cmake(KF6Wallet)
BuildRequires:  cmake(KF6WidgetsAddons)
BuildRequires:  cmake(KF6WindowSystem)
BuildRequires:  cmake(KF6XmlGui)
BuildRequires:  libacl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  switcheroo-control
BuildRequires:  zlib-devel
# built for this KIO: with a newer one the session keeps the stock dialog until this package is rebuilt
Requires:       kf6-kio-file-widgets%{?_isa} >= %{kio}

%description
Dialog NG is KDE's file dialog (the one KDE applications open to pick or save
a file, and that Firefox, Chrome and Flatpak applications get through the
desktop portal) with the look and the quick filters of Dolphin NG: rows with
the drawing of each kind of file, filters by kind, groups by date, a glass
sidebar.

Only one library changes, libKF6KIOFileWidgets, built from the same KIO
release Fedora ships and installed under %{ngprefix}. A file in
/etc/xdg/plasma-workspace/env puts it in front of the stock one for the
Plasma session, and only while the two versions match: after an update of
KDE Frameworks the stock dialog comes back until this package is rebuilt.
Log out and in once after installing.

%prep
%setup -q -T -b %{kiosource} -n kio-%{kio}
patch -p1 --no-backup-if-mismatch < %{SOURCE1}
# the help worker is not needed for the dialog
sed -i 's/^add_subdirectory( help )/# add_subdirectory( help )/' src/kioworkers/CMakeLists.txt

%build
%set_build_flags
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DBUILD_TESTING=OFF -DBUILD_DESIGNERPLUGIN=OFF -DCMAKE_SKIP_RPATH=ON
cmake --build build --target KF6KIOFileWidgets -j%{?_smp_build_ncpus}

%install
install -d %{buildroot}%{ngprefix}/%{_lib}
cp -a build/bin/libKF6KIOFileWidgets.so.6 build/bin/libKF6KIOFileWidgets.so.%{kio} %{buildroot}%{ngprefix}/%{_lib}/
install -d %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env
cat > %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/dialog-ng.sh <<'EOT'
# Dialog NG: KDE's file dialog with quick filters. Loaded only while it matches the installed KIO: after an
# update of KDE Frameworks the stock library is used again until the dialog-ng package is rebuilt.
ngdlg=/opt/ng/dialog-ng/lib64
if [ -e /usr/lib64/libKF6KIOFileWidgets.so.6 ] && [ -e "$ngdlg/libKF6KIOFileWidgets.so.6" ] &&
   [ "$(basename "$(readlink -f /usr/lib64/libKF6KIOFileWidgets.so.6)")" = "$(basename "$(readlink -f "$ngdlg/libKF6KIOFileWidgets.so.6")")" ]; then
    export LD_LIBRARY_PATH="$ngdlg${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
unset ngdlg
EOT

%files
%license LICENSES/*
%dir /opt/ng
%{ngprefix}
%config(noreplace) %{_sysconfdir}/xdg/plasma-workspace/env/dialog-ng.sh

%changelog
* Mon Nov 16 2026 Morzilla <3956663+Morzilla@users.noreply.github.com> - 6.32.0^202611161152gitd26d2cc-1
- Aurora port (light and dark), KIO 6.31 on Fedora 44 and 6.32 on Fedora 45

* Sat Nov 14 2026 Morzilla <3956663+Morzilla@users.noreply.github.com> - 6.31.0^202611122309git973ed26-1
- First package
