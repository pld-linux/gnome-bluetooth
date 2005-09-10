Summary:	GNOME Bluetooth Subsystem
Summary(pl):	Podsystem GNOME Bluetooth
Name:		gnome-bluetooth
Version:	0.6.0
Release:	3
License:	GPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/0.6/%{name}-%{version}.tar.gz
# Source0-md5:	19f55205ec977f22946088cfd3c4c7b4
Patch0:		%{name}-python.patch
Patch1:		%{name}-gnomeui.patch
Patch2:		%{name}-desktop.patch
Patch3:		%{name}-cleanup.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gob2 >= 2.0.8
BuildRequires:	libbtctl-devel >= 0.5
BuildRequires:	libgnomeui-devel
BuildRequires:	libtool
BuildRequires:	nautilus-devel
BuildRequires:	openobex-devel
BuildRequires:	python-btctl
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez-utils
Requires:	python-gnome-bonobo-ui
Requires:	python-gnome-canvas
Requires:	python-gnome-ui >= 2.0.0
Requires:	python-gnome-vfs
Requires:	python-pygtk-glade
%pyrequires_eq	python-libs
Obsoletes:	python-gnome-bluetooth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNOME Bluetooth Subsystem is being developed as a prototype by Edd
Dumbill, with the intention of being submitted to the GNOME desktop
project. The software is in its early stages right now.

This package contains a Bonobo server to control Bluetooth devices,
and a simple GUI to explore which devices are available
(gnome-bluetooth-admin). An OBEX server is available,
gnome-obex-server. This will receive files sent via Bluetooth to your
PC, and save them in your home directory. The program gnome-obex-send
enables you to send files. It is used by the gnome-vfs module - go to
bluetooth:/// in Nautilus and drag and drop a file onto a destination
device.

%description -l pl
GNOME Bluetooth Subsystem (podsystem GNOME Bluetooth) jest tworzony
przez Edda Dumbilla jako prototyp z zamiarem w³±czenia do projektu
GNOME. Na razie jest we wczesnym stadium rozwoju.

Ten pakiet zawiera serwer Bonobo do sterowania urz±dzeniami Bluetooth
oraz proste GUI do przegl±dania dostêpnych urz±dzeñ
(gnome-bluetooth-admin). Dostêpny jest serwer OBEX
(gnome-obex-server), pozwalaj±cy ¶ci±gaæ pliki wys³ane przez Bluetooth
do PC i zapisywaæ je w katalogu domowym. Program gnome-obex-send
pozwala wysy³aæ pliki. Jest u¿ywany przez modu³ gnome-vfs - wystarczy
wpisaæ bluetooth:/// w Nautilusie i przeci±gn±æ plik na urz±dzenie
docelowe.

%package libs
Summary:	GNOME bluetooth subsystem shared libraries
Summary(pl):	Wspó³dzielone biblioteki dla podsystemu GNOME bluetooth
Group:		Development/Libraries

%description libs
GNOME bluetooth subsystem shared libraries.

%description libs -l pl
Wspó³dzielone biblioteki dla podsystemu GNOME bluetooth.

%package devel
Summary:	Header files for GNOME bluetooth subsystem
Summary(pl):	Pliki nag³ówkowe dla podsystemu GNOME bluetooth
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for GNOME bluetooth subsystem.

%description devel -l pl
Pliki nag³ówkowe dla podsystemu GNOME bluetooth.

%package static
Summary:	Static GNOME bluetooth library
Summary(pl):	Statyczna biblioteka GNOME bluetooth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME bluetooth library.

%description static -l pl
Statyczna biblioteka GNOME bluetooth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

sed -i -e 's#$(PYTHON_PREFIX)/lib#$(PYTHON_PREFIX)/%{_lib}#g' python/Makefile.am

%build
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
cd libegg
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
cd ..
%configure \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{py_comp} $RPM_BUILD_ROOT%{py_sitedir}
%{py_ocomp} $RPM_BUILD_ROOT%{py_sitedir}

sed -i 's/manager.py$/manager.pyo/' $RPM_BUILD_ROOT%{_bindir}/gnome-bluetooth-manager
rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{a,la}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/gnomebt/*.{a,la,py}

%find_lang %{name} --with-gnome

%post
%gconf_schema_install gnome-obex-server.schemas

%preun
%gconf_schema_uninstall gnome-obex-server.schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_sysconfdir}/gconf/schemas/gnome-obex-server.schemas

%dir %{py_sitedir}/gnomebt
%attr(755,root,root) %{py_sitedir}/gnomebt/*.so
%{py_sitedir}/gnomebt/*.pyc
%{py_sitedir}/gnomebt/*.pyo

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_pkgconfigdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
