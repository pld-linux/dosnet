#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
%define		_moddir		/lib/modules/%{_kernel_ver}/misc
%define		_moddirsmp	/lib/modules/%{_kernel_ver}smp/misc
Summary:	A DOS emulator
Summary(de):	DOS-Emulator
Summary(es):	Emulador DOS
Summary(fr):	Emulateur DOS
Summary(pl):	Emulator DOS-a
Summary(pt_BR):	Emulador DOS
Summary(tr):	DOS öykünümcüsü
Name:		dosnet
Version:	1.0.2
%define	_rel	22
Release:	%{_rel}
Epoch:		1
License:	GPL v2
Group:		Applications/Emulators
Source0:	dosnet-%{version}.tar.gz
# Source0-md5:	4932fa14e221071dafaae48656d35658
ExclusiveArch:	%{ix86}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel < 2.0.28

%description
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection between dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -l pl
Modu³ dosnet.o dla kernela. Modu³ ten pozwala ³±czyæ siê programom
DOS-owym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi
przy pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na
temat dosnet mo¿esz znale¼æ w README do dosemu.

%package -n kernel-net-dosnet
Summary:	Kernel module dosnet.o
Summary(pl):	Modu³ j±dra dosnet.o
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
#Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-net-dosnet
Kernel module for dosnet (vnet). Dosnet lets you establish TCP/IP
connection between dosemu session and Linux kernel. Read README for
dosemu for more information.

%description -n kernel-net-dosnet -l pl
Modu³ j±dra dosnet.o. Modu³ ten pozwala ³±czyæ siê programom DOS-owym
wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy innymi przy
pisaniu programów sieciowych dla DOS-a. Rzeteln± informacjê na temat
dosnet mo¿na znale¼æ w README do dosemu.

%package -n kernel-smp-net-dosnet
Summary:	SMP kernel module dosnet.o
Summary(pl):	Wersja SMP modu³u j±dra dosnet.o
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
#Requires:	%{name} = %{version}
Obsoletes:	dosnet

%description -n kernel-smp-net-dosnet
SMP version of kernel module for dosnet (vnet). Dosnet lets you
establish TCP/IP connection between dosemu session and Linux
kernel. Read README for dosemu for more information.

%description -n kernel-smp-net-dosnet -l pl
Wersja SMP modu³u j±dra dosnet.o. Modu³ ten pozwala ³±czyæ siê
programom DOS-owym wykorzystuj±cym TCP/IP z Linuksem. Przydatny miêdzy
innymi przy pisaniu programów sieciowych dla DOS-a. Rzeteln±
informacjê na temat dosnet mo¿na znale¼æ w README do dosemu.

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
%depmod %{_kernel_ver}

%postun	-n kernel-net-dosnet
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-dosnet
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-dosnet
%depmod %{_kernel_ver}smp

%files -n kernel-net-dosnet
%defattr(644,root,root,755)
%{_moddir}/dosnet.o*

%files -n kernel-smp-net-dosnet
%defattr(644,root,root,755)
%{_moddirsmp}/dosnet.o*
