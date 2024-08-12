#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	46.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-bluetooth/46/%{name}-%{version}.tar.xz
# Source0-md5:	6f1f8e6b51c4903727ef41ec6c398f13
Source1:	61-%{name}-rfkill.rules
URL:		https://wiki.gnome.org/Projects/GnomeBluetooth
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gsound-devel
BuildRequires:	gtk4-devel >= 4.4
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	libadwaita-devel >= 1.4
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libxml2-progs
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	upower-devel >= 0.99.14
BuildRequires:	xz
Requires:	gnome-bluetooth3-libs = %{version}-%{release}
Requires:	gnome-bluetooth3-ui-libs = %{version}-%{release}
Requires:	bluez >= 4.22
Requires:	dbus(org.openobex.client)
Requires:	dconf
Requires:	hicolor-icon-theme
Requires:	udev-acl
Obsoletes:	bluez-gnome < 1.9
Obsoletes:	bluez-pin < 0.31
Obsoletes:	nautilus-sendto-gnome-bluetooth < 3.8
Obsoletes:	python-gnome-bluetooth < 0.5.1-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Bluetooth provides tools for controlling and communicating with
Bluetooth devices.

%description -l pl.UTF-8
GNOME Bluetooth dostarcza narzędzia do kontrolowania i komunikowania
się z urządzeniami Bluetooth.

%package -n gnome-bluetooth3-libs
Summary:	GNOME Bluetooth 3.0 subsystem shared library
Summary(pl.UTF-8):	Biblioteka współdzielona podsystemu GNOME Bluetooth 3.0
License:	LGPL v2+
Group:		Libraries
Requires:	glib2 >= 1:2.44
Requires:	upower-libs >= 0.99.14

%description -n gnome-bluetooth3-libs
GNOME Bluetooth 3.0 subsystem shared library.

%description -n gnome-bluetooth3-libs -l pl.UTF-8
Biblioteka współdzielona podsystemu GNOME Bluetooth 3.0.

%package -n gnome-bluetooth3-devel
Summary:	Header files for GNOME Bluetooth 3.0 subsystem
Summary(pl.UTF-8):	Pliki nagłówkowe podsystemu GNOME Bluetooth 3.0
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	gnome-bluetooth3-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Obsoletes:	gnome-bluetooth-static < 3.32

%description -n gnome-bluetooth3-devel
Header files for GNOME Bluetooth 3.0 subsystem.

%description -n gnome-bluetooth3-devel -l pl.UTF-8
Pliki nagłówkowe podsystemu GNOME Bluetooth 3.0.

%package -n gnome-bluetooth3-ui-libs
Summary:	GNOME Bluetooth 3.0 subsystem UI shared library
Summary(pl.UTF-8):	Współdzielone biblioteki UI podsystemu GNOME Bluetooth 3.0
License:	LGPL v2+
Group:		X11/Libraries
Requires:	gnome-bluetooth3-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.44
Requires:	gtk4 >= 4.4
Requires:	libadwaita >= 1.4
Requires:	libnotify-devel >= 0.7.0
Requires:	upower-libs >= 0.99.14

%description -n gnome-bluetooth3-ui-libs
GNOME Bluetooth 3.0 subsystem UI shared library.

%description -n gnome-bluetooth3-ui-libs -l pl.UTF-8
Współdzielone biblioteki UI podsystemu GNOME Bluetooth 3.0.

%package -n gnome-bluetooth3-ui-devel
Summary:	Header files for GNOME Bluetooth 3.0 subsystem UI
Summary(pl.UTF-8):	Pliki nagłówkowe UI podsystemu GNOME Bluetooth 3.0
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	gnome-bluetooth3-devel = %{version}-%{release}
Requires:	gnome-bluetooth3-ui-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	gtk4-devel >= 4.4
Requires:	libadwaita-devel >= 1.4

%description -n gnome-bluetooth3-ui-devel
Header files for GNOME Bluetooth 3.0 subsystem UI.

%description -n gnome-bluetooth3-ui-devel -l pl.UTF-8
Pliki nagłówkowe UI podsystemu GNOME Bluetooth 3.0.

%package -n gnome-bluetooth3-apidocs
Summary:	GNOME Bluetooth 3.0 library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNOME Bluetooth 3.0
Group:		Documentation
BuildArch:	noarch

%description -n gnome-bluetooth3-apidocs
GNOME Bluetooth library API documentation.

%description -n gnome-bluetooth3-apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNOME Bluetooth.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/udev/rules.d

%ninja_install -C build

cp -p %{SOURCE1} $RPM_BUILD_ROOT/lib/udev/rules.d

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n gnome-bluetooth3-libs -p /sbin/ldconfig
%postun	-n gnome-bluetooth3-libs -p /sbin/ldconfig

%post	-n gnome-bluetooth3-ui-libs -p /sbin/ldconfig
%postun	-n gnome-bluetooth3-ui-libs -p /sbin/ldconfig

%files -f %{name}-3.0.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/bluetooth-sendto
%{_desktopdir}/bluetooth-sendto.desktop
%{_mandir}/man1/bluetooth-sendto.1*
/lib/udev/rules.d/61-gnome-bluetooth-rfkill.rules

%files -n gnome-bluetooth3-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth-3.0.so.13
%{_libdir}/girepository-1.0/GnomeBluetooth-3.0.typelib
%{_datadir}/gnome-bluetooth-3.0

%files -n gnome-bluetooth3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth-3.0.so
# no C headers here
%{_datadir}/gir-1.0/GnomeBluetooth-3.0.gir
%{_pkgconfigdir}/gnome-bluetooth-3.0.pc

%files -n gnome-bluetooth3-ui-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth-ui-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth-ui-3.0.so.13

%files -n gnome-bluetooth3-ui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth-ui-3.0.so
%dir %{_includedir}/gnome-bluetooth-3.0
%{_includedir}/gnome-bluetooth-3.0/bluetooth-settings-widget.h
%{_pkgconfigdir}/gnome-bluetooth-ui-3.0.pc

%if %{with apidocs}
%files -n gnome-bluetooth3-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth-3.0
%endif
