Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	2.27.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/2.27/%{name}-%{version}.tar.bz2
# Source0-md5:	4a7c977086af47fe43ea08b29ab93503
URL:		http://live.gnome.org/GnomeBluetooth
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.9
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	hal-devel >= 0.5.10
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	unique-devel >= 1.0.0
Requires(post,postun):	gtk+2
Requires(post,preun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez >= 4.22
Requires:	hicolor-icon-theme
Requires:	obex-data-server
Obsoletes:	python-gnome-bluetooth
Conflicts:	bluez-gnome
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
Requires:	dbus-glib-devel >= 0.74
Requires:	gtk+2-devel >= 2:2.14.0

%description devel
Header files for GNOME Bluetooth subsystem.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla podsystemu GNOME Bluetooth.

%package static
Summary:	Static GNOME Bluetooth library
Summary(pl.UTF-8):	Statyczna biblioteka GNOME Bluetooth
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME Bluetooth library.

%description static -l pl.UTF-8
Statyczna biblioteka GNOME Bluetooth.

%package apidocs
Summary:	GNOME Bluetooth library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNOME Bluetooth
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME Bluetooth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNOME Bluetooth.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-static \
	--disable-desktop-update \
	--disable-icon-update \
	--disable-schemas-install \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/mus

%find_lang %{name}2

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%gconf_schema_install bluetooth-manager.schemas

%preun
%gconf_schema_uninstall bluetooth-manager.schemas

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}2.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/bluetooth-applet
%attr(755,root,root) %{_bindir}/bluetooth-properties
%attr(755,root,root) %{_bindir}/bluetooth-sendto
%attr(755,root,root) %{_bindir}/bluetooth-wizard
%{_desktopdir}/bluetooth-properties.desktop
%{_sysconfdir}/gconf/schemas/bluetooth-manager.schemas
%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop
%{_datadir}/gnome-bluetooth
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/bluetooth-applet.1*
%{_mandir}/man1/bluetooth-properties.1*
%{_mandir}/man1/bluetooth-sendto.1*
%{_mandir}/man1/bluetooth-wizard.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so
%{_libdir}/libgnome-bluetooth.la
%{_includedir}/gnome-bluetooth
%{_pkgconfigdir}/gnome-bluetooth-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnome-bluetooth.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth
