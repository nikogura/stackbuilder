Name: stackbuilder
Summary: Build framework for creating stacks of disparate software
Version: __VERSION__
Release: 1
Group: Development/Tools
Source: __TARBALL__
URL: https://github.com/nikogura/stackbuilder
Distribution: Linux
Vendor: None
Packager: Nik Ogura <nik.ogura@gmail.com>
License: Apache 2.0
AutoReqProv: no

%description
Stackbuilder is a framework written in python to consume the 'stack' section of an stack.yaml which specifies a
list of components that come from various sources and must be built into a common location.  A good example is
a LAMP stack that requires Apache, connectors such as mod_wsgi, Python, etc for an app to run in the absence of
distro provided rpms.  Obviously if the distro provided appropriate packages, Stackbuilder wouldn't be required, but
an appropriate version of a distro isn't always available.

Stackbuilder stacks are designed to build and install into a complete space.  Multiple Stackbuilder stacks on a system will
likely result in duplication, but disk space is cheap and an app needs to be able to deploy and upgrade without
interference with it's potential neighbors

%prep
rm -rf $RPM_BUILD_DIR/*
rm -rf $RPM_BUILD_ROOT/*

#tar xzvf $RPM_SOURCE_DIR/__TARBALL__ -C $RPM_BUILD_DIR

%build
mkdir -p $RPM_BUILD_ROOT
tar xzvf $RPM_SOURCE_DIR/__TARBALL__ -C $RPM_BUILD_ROOT
#cp -r $RPM_BUILD_DIR/* $RPM_BUILD_ROOT

%files
/opt/stackbuilder

%post
ln -sf /opt/stackbuilder/bin/stackbuilder.sh /etc/profile.d/stackbuilder.sh
source /etc/profile.d/stackbuilder.sh

%postun
if [ "$1 = 0" ]; then
rm -f /etc/profile.d/stackbuilder.sh
fi
