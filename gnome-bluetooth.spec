Summary:	GNOME Bluetooth Subsystem
Name:		gnome-bluetooth
Version:	0.4.1
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://usefulinc.com/software/gnome-bluetooth/releases/%{name}-%{version}.tar.gz
# Source0-md5:	59d83693ee5e10fed0aa7c941b0423d9
URL:		http://usefulinc.com/software/gnome-bluetooth/
BuildRequires:	libbtctl-devel >= 0.3
BuildRequires:	gob2 >= 2.0.6
BuildRequires:	libgnomeui-devel
BuildRequires:	nautilus-devel
Requires:	bluez-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Bluetooth Subsystem.

%prep
%setup -q

%build
rm -f missing
glib-gettextize --copy --force
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/gnome-bluetooth-control
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libbluetooth
%{_libdir}/gnome-vfs-2.0/modules/libbluetooth.la
%{_libdir}/bonobo/servers/*
%{_datadir}/%{name}
%{_datadir}/idl/*
%{_desktopdir}/*
