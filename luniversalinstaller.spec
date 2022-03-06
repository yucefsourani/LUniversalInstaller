Name:           luniversalinstaller
Version:        0.2
Release:        18%{?dist}
Summary:        Python+Gtk Universal Installer
License:        GPLv3     
URL:            https://github.com/yucefsourani/LUniversalInstaller
Source0:        https://github.com/yucefsourani/LUniversalInstaller/archive/master.zip
BuildArch:      noarch
BuildRequires:  python3-devel
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
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --prefix /usr


%files
%doc README.md
%{python3_sitelib}/*
%{_bindir}/luniversalinstaller.py
%{_datadir}/applications/*
%{_datadir}/luniversalinstaller/plugins/*
%{_datadir}/luniversalinstaller/images/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/doc/luniversalinstaller/LICENSE

%changelog
* Sun Mar 6 2022 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-18
- Release 18

* Tue Sep 28 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-17
- Release 17
- Add Brave Browser
- Add Microsoft Edge Beta

* Sun Sep 26 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-16
- Release 16
- Support fedora 35

* Mon Apr 26 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-15
- Release 15

* Thu Mar 25 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-14
- Release 14

* Thu Mar 16 2021 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-13
- Release 13

* Wed Oct 28 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-12
- Release 12
- Add anydesk plugin

* Mon Oct 19 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-11
- Release 11

* Sat Jul 25 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-10
- Release 10
- Update xdman plugin to new version

* Thu Mar 24 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-9
- Release 9

* Fri Mar 13 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-8
- Release 8
- Fix xdman plugin 

* Fri Jan 17 2020 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-7
- Release 7
- Fix intellij_idea Plugin For Fedora 31 32

* Fri Oct 25 2019 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-6
- Release 6
- Fix Codecs Plugin For Fedora 32

* Sat Sep 21 2019 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-5
- Release 5
- Fix Netbeans Plugin For Fedora 31

* Thu Jun 6 2019 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-4
- Release 4

* Mon Jan 14 2019 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-3
- Release 3

* Mon Jan 14 2019 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-2
- Release 2

* Wed Oct 31 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.2-1
- Version 0.2 

* Wed Oct 31 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-9
- Release 9 

* Tue Oct 30 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-8
- Release 8 

* Sat Oct 13 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-7
- Release 7 

* Wed Oct 03 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-6
- Release 6 

* Fri Sep 28 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-5
- Release 5 

* Fri Sep 28 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-4
- Release 4 

* Fri Sep 28 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-3
- Release 3 

* Thu Sep 27 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-2
- Release 2 

* Tue Sep 25 2018 yucuf sourani <youssef.m.sourani@gmail.com> 0.1-1
- Initial For Fedora 
