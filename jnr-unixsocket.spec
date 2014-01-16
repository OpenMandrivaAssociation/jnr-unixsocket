%{?_javapackages_macros:%_javapackages_macros}
Name:           jnr-unixsocket
Version:        0.2
Release:        2.0%{?dist}
Summary:        Unix sockets for Java

License:        ASL 2.0
URL:            http://github.com/jnr/%{name}/
Source0:        https://github.com/jnr/%{name}/archive/%{version}.tar.gz/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jnr-constants
BuildRequires:  jnr-enxio
BuildRequires:  jnr-ffi

BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4

%description
Unix sockets for Java.

%package javadoc
Summary:        Javadocs for %{name}


%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

# remove unnecessary wagon extension
%pom_xpath_remove pom:build/pom:extensions

find ./ -name '*.jar' -delete 
find ./ -name '*.class' -delete

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 11 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2-1
- Initial package.
