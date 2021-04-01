#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	3.34.5
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-bluetooth/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	d83faa54abaf64bb40b5313bc233e74e
Source1:	61-%{name}-rfkill.rules
URL:		https://wiki.gnome.org/Projects/GnomeBluetooth
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.12.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libxml2-progs
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.38.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
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

%package libs
Summary:	GNOME Bluetooth subsystem shared libraries
Summary(pl.UTF-8):	Współdzielone biblioteki dla podsystemu GNOME Bluetooth
License:	LGPL v2+
Group:		X11/Libraries
Requires:	glib2 >= 1:2.38.0
Requires:	gtk+3 >= 3.12.0
Requires:	libnotify >= 0.7.0

%description libs
GNOME Bluetooth subsystem shared libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki dla podsystemu GNOME Bluetooth.

%package devel
Summary:	Header files for GNOME Bluetooth subsystem
Summary(pl.UTF-8):	Pliki nagłówkowe dla podsystemu GNOME Bluetooth
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38.0
Requires:	gtk+3-devel >= 3.12.0
Obsoletes:	gnome-bluetooth-static < 3.32

%description devel
Header files for GNOME Bluetooth subsystem.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla podsystemu GNOME Bluetooth.

%package apidocs
Summary:	GNOME Bluetooth library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNOME Bluetooth
Group:		Documentation
BuildArch:	noarch

%description apidocs
GNOME Bluetooth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNOME Bluetooth.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dicon_update=false

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/udev/rules.d

%ninja_install -C build

cp -p %{SOURCE1} $RPM_BUILD_ROOT/lib/udev/rules.d

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/bluetooth-sendto
%{_desktopdir}/bluetooth-sendto.desktop
%{_datadir}/gnome-bluetooth
%{_iconsdir}/hicolor/*x*/apps/bluetooth.png
%{_iconsdir}/hicolor/*x*/status/bluetooth-*.png
%{_iconsdir}/hicolor/scalable/apps/bluetooth.svg
%{_iconsdir}/hicolor/scalable/status/bluetooth-*.svg
%{_mandir}/man1/bluetooth-sendto.1*
/lib/udev/rules.d/61-gnome-bluetooth-rfkill.rules

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth.so.13
%{_libdir}/girepository-1.0/GnomeBluetooth-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so
%{_includedir}/gnome-bluetooth
%{_pkgconfigdir}/gnome-bluetooth-1.0.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth
%endif
