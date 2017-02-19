Summary:	GNOME Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	3.20.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/3.20/%{name}-%{version}.tar.xz
# Source0-md5:	0768931f17eaba8b05eddacf17204f60
Source1:	61-%{name}-rfkill.rules
URL:		http://live.gnome.org/GnomeBluetooth
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.11.2
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	udev-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
Requires(post,postun):	glib2 >= 1:2.38.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez >= 4.22
Requires:	dbus(org.openobex.client)
Requires:	dconf
Requires:	hicolor-icon-theme
Requires:	udev-acl
Obsoletes:	bluez-gnome < 1.9
Obsoletes:	bluez-pin
Obsoletes:	nautilus-sendto-gnome-bluetooth
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
Requires:	udev-devel

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-desktop-update \
	--disable-icon-update \
	--enable-introspection \
	--disable-schemas-compile \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/udev/rules.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/lib/udev/rules.d

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgnome-bluetooth.la

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
%attr(755,root,root) %{_bindir}/bluetooth-sendto
%{_desktopdir}/bluetooth-sendto.desktop
%{_datadir}/gnome-bluetooth
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
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

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gnome-bluetooth
