%define		_moddir		/lib/modules/%{_kernel_ver}/misc
%define		_moddirsmp	/lib/modules/%{_kernel_ver}smp/misc
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOSa
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS öykünümcüsü
Name:		dosnet
Version:	1.0.2
%define	_rel	21
Release:	%{_rel}
Epoch:		1
License:	GPL v2
Group:		Applications/Emulators
Source0:	dosnet-%{version}.tar.gz
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28

%description
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection between dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

%package -n kernel-net-dosnet
Summary:	kernel module dosnet.o
Summary(pl):	Modu³ dosnet.o do kernela
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
#Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection between dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -n kernel-net-dosnet -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

%package -n kernel-smp-net-dosnet
Summary:	kernel-smp module dosnet.o
Summary(pl):	Modu³ dosnet.o do kernela SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
#Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-smp-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection between dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -n kernel-smp-net-dosnet -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOSowym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

%prep
%setup -q -n dosnet

%build
OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"; export OPTFLAGS

%{__cc} $OPTFLAGS -I%{_includedir} -D__KERNEL__ -D__KERNEL_SMP=1 \
	-Wall -Wstrict-prototypes \
	-fno-strength-reduce -I%{_kernelsrcdir}/include \
	-DMODULE \
	-c -o dosnet.o dosnet.c
mkdir smp
mv -f dosnet.o smp/

%{__cc} $OPTFLAGS -I%{_includedir} -D__KERNEL__ \
	-Wall -Wstrict-prototypes \
	-fno-strength-reduce -I%{_kernelsrcdir}/include \
	-DMODULE \
	-c -o dosnet.o dosnet.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_moddir},%{_moddirsmp}}
install dosnet.o $RPM_BUILD_ROOT%{_moddir}
install smp/dosnet.o $RPM_BUILD_ROOT%{_moddirsmp}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-dosnet
/sbin/depmod -a

%postun	-n kernel-net-dosnet
/sbin/depmod -a

%post	-n kernel-smp-net-dosnet
/sbin/depmod -a

%postun	-n kernel-smp-net-dosnet
/sbin/depmod -a

%files -n kernel-net-dosnet
%defattr(644,root,root,755)
%{_moddir}/dosnet.o*

%files -n kernel-smp-net-dosnet
%defattr(644,root,root,755)
%{_moddirsmp}/dosnet.o*
