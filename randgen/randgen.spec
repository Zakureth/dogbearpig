Name:           randgen
Version:        1.0
Release:        4%{?dist}
Summary:        Dual-mode random generator for passwords (rpg) and usernames (rug)

License:        MIT
URL:            https://github.com/Zakureth/dogbearpig/randgen
Source0:        randgen.py
Source1:        rpg.1
Source2:        rug.1
Source3:        populate_randgen_words.py
Source4:        verbs.txt
Source5:        nouns.txt
Source6:        adjectives.txt
Source7:        adverbs.txt

BuildArch:      noarch
Requires:       python3

%description
Installs two commands:
- rpg: random password generator (Adverb-Verb-Number or Adverb-Verb-Noun-Number)
- rug: random username generator (AdjectiveNounNumber)

Word lists are installed to /usr/share/randgen.

%prep
%setup -q -c -T
cp %{SOURCE0} randgen.py
cp %{SOURCE1} rpg.1
cp %{SOURCE2} rug.1
cp %{SOURCE3} populate_randgen_words.py
cp %{SOURCE4} verbs.txt
cp %{SOURCE5} nouns.txt
cp %{SOURCE6} adjectives.txt
cp %{SOURCE7} adverbs.txt

%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 randgen.py %{buildroot}%{_bindir}/rpg
ln %{buildroot}%{_bindir}/rpg %{buildroot}%{_bindir}/rug

mkdir -p %{buildroot}%{_mandir}/man1
install -m0644 rpg.1 %{buildroot}%{_mandir}/man1/rpg.1.gz
install -m0644 rug.1 %{buildroot}%{_mandir}/man1/rug.1.gz

mkdir -p %{buildroot}/usr/share/randgen
install -m0644 verbs.txt %{buildroot}/usr/share/randgen/verbs.txt
install -m0644 nouns.txt %{buildroot}/usr/share/randgen/nouns.txt
install -m0644 adjectives.txt %{buildroot}/usr/share/randgen/adjectives.txt
install -m0644 adverbs.txt %{buildroot}/usr/share/randgen/adverbs.txt

%files
%{_bindir}/rpg
%{_bindir}/rug
%{_mandir}/man1/rpg.1.gz
%{_mandir}/man1/rug.1.gz
/usr/share/randgen/*.txt

%changelog
* Sun Jul 13 2025 Michael <zakureth@gmail.com> - 1.0-4
- Reworked password format logic and wordlist packaging

