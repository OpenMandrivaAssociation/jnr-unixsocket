%bcond_with javadoc
Name:           jnr-unixsocket
Version:        0.39.8
Release:        1
Summary:        Unix sockets for Java

License:        ASL 2.0
URL:            https://github.com/jnr/%{name}/
Source0:        https://github.com/jnr/%{name}/archive/refs/tags/jnr-unixsocket-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

BuildRequires:  jnr-parent
BuildRequires:  jnr-constants
BuildRequires:  jnr-enxio
BuildRequires:  jnr-ffi

%description
Unix sockets for Java.

%if %{with javadoc}
%package javadoc
Summary:        Javadocs for %{name}


%endif
%if %{with javadoc}
%description javadoc
This package contains the API documentation for %{name}.

%endif
%prep
%setup -q -n jnr-unixsocket-jnr-unixsocket-%{version}

find ./ -name '*.jar' -delete
find ./ -name '*.class' -delete
# bnd's wildcard import reads a bundle version from every jar. ASM has none.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(r"\s*<manifestFile>.*?</manifestFile>", "", text, count=1, flags=re.S)
# The assembly execution builds a fat jar. The package uses the system jars.
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.maven\.plugins</groupId>\s*<artifactId>maven-assembly-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
# jnr-parent configures surefire with a JDK toolchain that is not installed.
plugin = """      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration combine.self="override"/>
      </plugin>
"""
marker = "</plugins>"
text = text[:text.rfind(marker)] + plugin + text[text.rfind(marker):]
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE

%endif
