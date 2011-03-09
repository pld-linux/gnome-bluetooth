Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	2.91.91
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/2.91/%{name}-%{version}.tar.bz2
# Source0-md5:	43b00d0ad7136641779d9e9a201340d6
URL:		http://live.gnome.org/GnomeBluetooth
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common
BuildRequires:	gnome-control-center-devel >= 2.91.90
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	nautilus-sendto-devel >= 2.91.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez >= 4.22
Requires:	dbus(org.openobex.client)
Requires:	dbus-glib
Requires:	dconf
Requires:	hicolor-icon-theme
Obsoletes:	bluez-gnome < 1.9
Obsoletes:	bluez-pin
Obsoletes:	python-gnome-bluetooth
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
Requires:	gtk+3-devel >= 3.0.0

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

%package -n nautilus-sendto-gnome-bluetooth
Summary:	nautilus-sendto GNOME Bluetooth plugin
Summary(pl.UTF-8):	Wtyczka nautilus-sendto dla GNOME Bluetooth
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus-sendto >= 2.91.0

%description -n nautilus-sendto-gnome-bluetooth
A nautilus-sendto plugin for sending files via GNOME Bluetooth.

%description -n nautilus-sendto-gnome-bluetooth -l pl.UTF-8
Wtyczka nautilus-sentdo do wysyłania plików poprzez GNOME Bluetooth.

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
	--disable-desktop-update \
	--disable-icon-update \
	--enable-introspection \
	--disable-schemas-compile \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnome-bluetooth.la \
        $RPM_BUILD_ROOT%{_libdir}/gnome-bluetooth/plugins/*.la \
        $RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/libbluetooth.la \
        $RPM_BUILD_ROOT%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.la \
        $RPM_BUILD_ROOT%{_libdir}/nautilus-sendto/plugins/libnstbluetooth.la

# workaround for (broken?) GnomeBluetoothApplet-1.0.typelib
ln -s %{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.0 $RPM_BUILD_ROOT%{_libdir}/libgnome-bluetooth-applet.so.0

%find_lang %{name} --with-gnome --with-omf --all-name

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/bluetooth-applet
%attr(755,root,root) %{_bindir}/bluetooth-sendto
%attr(755,root,root) %{_bindir}/bluetooth-wizard
%{_desktopdir}/bluetooth-properties.desktop
%{_desktopdir}/bluetooth-sendto.desktop
%{_desktopdir}/bluetooth-wizard.desktop
%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop
%{_datadir}/GConf/gsettings/gnome-bluetooth*
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/gnome-bluetooth
%attr(755,root,root) %{_libdir}/control-center-1/panels/libbluetooth.so
%dir %{_libdir}/gnome-bluetooth/plugins
%attr(755,root,root) %{_libdir}/gnome-bluetooth/plugins/*.so
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/bluetooth-applet.1*
%{_mandir}/man1/bluetooth-sendto.1*
%{_mandir}/man1/bluetooth-wizard.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnome-bluetooth.so.8
%dir %{_libdir}/gnome-bluetooth
%attr(755,root,root) %{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so
%attr(755,root,root) %{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.0
%attr(755,root,root) %{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.*.*.*
%attr(755,root,root) %{_libdir}/libgnome-bluetooth-applet.so.0
%{_libdir}/gnome-bluetooth/GnomeBluetoothApplet-1.0.typelib
%{_libdir}/girepository-1.0/GnomeBluetooth-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-bluetooth.so
%{_includedir}/gnome-bluetooth
%{_pkgconfigdir}/gnome-bluetooth-1.0.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth

%files -n nautilus-sendto-gnome-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus-sendto/plugins/libnstbluetooth.so
