%{?_javapackages_macros:%_javapackages_macros}
Name:          kryo
Version:       3.0.3
Release:       3%{?dist}
Summary:       Object graph serialization framework for Java
# ASL: src/com/esotericsoftware/kryo/util/IdentityMap.java src/com/esotericsoftware/kryo/util/IntMap.java
License:       ASL 2.0 and BSD
Url:           https://github.com/EsotericSoftware/kryo
Source0:       https://github.com/EsotericSoftware/kryo/archive/%{name}-parent-%{version}.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: maven-local
BuildRequires: mvn(com.esotericsoftware:minlog)
BuildRequires: mvn(com.esotericsoftware:reflectasm)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.objenesis:objenesis)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
Kryo is a fast and efficient object graph serialization framework for Java.
The goals of the project are speed, efficiency, and an easy to use API.
The project is useful any time objects need to be persisted, whether to a
file, database, or over the network.

Kryo can also perform automatic deep and shallow copying/cloning.
This is direct copying from object to object, not object->bytes->object.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-parent-%{version}
find . -name "*.class" -delete
find . -name "*.jar" -delete

# Do not shaded reflectasm
%pom_disable_module pom-shaded.xml

%pom_remove_plugin :maven-assembly-plugin pom-main.xml
%pom_remove_plugin :clirr-maven-plugin pom-main.xml

%pom_remove_plugin :maven-bundle-plugin pom-main.xml
%pom_add_plugin org.apache.felix:maven-bundle-plugin pom-main.xml "
<extensions>true</extensions>
<configuration>
  <instructions>
    <Import-Package>sun.reflect;resolution:=optional,*</Import-Package>
    <Export-Package>com.esotericsoftware.kryo.*</Export-Package>
  </instructions>
</configuration>"

# remove shaded deps
%pom_xpath_remove "pom:dependency[pom:classifier = 'shaded']"

cp -p %{SOURCE1} .
sed -i 's/\r//' license.txt LICENSE-2.0.txt

%mvn_file :%{name} %{name}
%mvn_alias :%{name} "com.esotericsoftware.%{name}:%{name}"

%build

# Test on arm builder fails, see RHBZ#991712
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc CHANGES.md README.md
%doc license.txt LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc license.txt LICENSE-2.0.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 gil cattaneo <puntogil@libero.it> 3.0.3-1
- update to 3.0.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 gil cattaneo <puntogil@libero.it> 3.0.1-1
- update to 3.0.1

* Fri Mar 13 2015 gil cattaneo <puntogil@libero.it> 2.22-4
- fix Url and Source0 tag

* Mon Feb 09 2015 gil cattaneo <puntogil@libero.it> 2.22-3
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 09 2013 gil cattaneo <puntogil@libero.it> 2.22-1
- update to 2.22

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 2.21-2
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Mar 28 2013 gil cattaneo <puntogil@libero.it> 2.21-1
- update to 2.21

* Thu Aug 4 2011 gil <puntogil@libero.it> 1.04-mga1
- initial rpm
