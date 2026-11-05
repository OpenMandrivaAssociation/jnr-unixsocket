%bcond_with javadoc
Name:           jnr-unixsocket
Version:        0.39.8
Release:        1
Summary:        Unix sockets for Java
Group:          Development/Java
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
BuildRequires:  jnr-posix
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
text = text.replace(
	"<artifactId>maven-jar-plugin</artifactId>",
	"<artifactId>maven-jar-plugin</artifactId>\n        <version>3.3.0</version>",
	1,
)
# The assembly execution builds a fat jar. The package uses the system jars.
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.maven\.plugins</groupId>\s*<artifactId>maven-assembly-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
# pluginManagement is what a child inherits. An empty configuration
# replaces jnr-parent's JDK toolchain, which runs even when tests are skipped.
text = text.replace(
	"<build>",
	"""<build>
    <pluginManagement>
      <plugins>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <configuration combine.self="override"/>
        </plugin>
      </plugins>
    </pluginManagement>""",
	1,
)
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE

%endif
