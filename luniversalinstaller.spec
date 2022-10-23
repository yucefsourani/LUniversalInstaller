Name:           luniversalinstaller
Version:        0.2
Release:        22%{?dist}
Summary:        Python+Gtk Universal Installer
License:        GPLv3     
URL:            https://github.com/yucefsourani/LUniversalInstaller
Source0:        https://github.com/yucefsourani/LUniversalInstaller/archive/master.zip
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  meson
Requires:       vte291
#Requires:       pygobject3
Requires:       python3-gobject
Requires:       gtk3
Requires:       python3-beautifulsoup4
Requires:       flatpak
Requires:       gnome-icon-theme

%description
Python+Gtk Universal Installer.


%prep
%autosetup -n LUniversalInstaller-master

%build
%meson

%install
rm -rf $RPM_BUILD_ROOT
%meson_install


%files
%doc README.md
%{_bindir}/luniversalinstaller.py
%{_datadir}/applications/*
%{_datadir}/luniversalinstaller/plugins/*
%{_datadir}/luniversalinstaller/images/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/doc/luniversalinstaller/LICENSE

%changelog
* Thu Oct 20 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-22
- Release 22

* Thu Oct 20 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-21
- Release 21
- Support fedora 37
- meson build

* Thu Apr 21 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-20
- Release 20
- Update Xdman To v7.2.10

* Sun Mar 6 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-19
- Release 19

* Sun Mar 6 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-18
- Release 18

* Tue Sep 28 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-17
- Release 17
- Add Brave Browser
- Add Microsoft Edge Beta

