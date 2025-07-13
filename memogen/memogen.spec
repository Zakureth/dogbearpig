Name:           memogen
Version:        1.0
Release:        1%{?dist}
Summary:        Multi‐mode random generator for passwords (rpg) and usernames (rug)

License:        MIT
URL:            https://github.com/Zakureth/dogbearpig/memogen
Source0:        memogen.py

BuildArch:      noarch
Requires:       python3
Requires:       python3-requests

%description
Installs a single script that behaves as:
- rpg: random password generator (verb-adverb-noun variants)
- rug: random username generator (adjective-noun-number)
Cached word lists live in ~/.adjustwords/wordbank.json. 

%prep
# no prep needed

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 memogen.py %{buildroot}%{_bindir}/memogen
ln -s memogen %{buildroot}%{_bindir}/rpg
ln -s memogen %{buildroot}%{_bindir}/rug

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 rpg.1 %{buildroot}%{_mandir}/man1/
install -m 0644 rug.1 %{buildroot}%{_mandir}/man1/

%files
%{_bindir}/memogen
%{_bindir}/rpg
%{_bindir}/rug
%{_mandir}/man1/rpg.1
%{_mandir}/man1/rug.1
%doc README.md LICENSE

%changelog
* Sun Jul 13 2025 Michael <zakureth@gmail.com> - 1.0-1
- initial package
