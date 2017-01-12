#!/usr/bin/env bash
set -e

BUILDNUMBER=$1

echo "clean the workspace"
rm -f *gz

wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh epel-release-6-8.noarch.rpm

echo "Installing Packages"
sudo yum install -y \
autoconf \
bison \
flex \
gcc \
gcc-c++ \
kernel-devel \
make \
m4 \
patch \
gettext-devel \
zlib-devel \
bzip2-devel \
bc \
PyYAML \
python-gnupg \
python-requests \
rpmbuild \
rpmdevtools

if (( $(bc <<< "$(cat /etc/redhat-release | cut -d " " -f7) > 7") )); then
    echo "Installing Optional Packages"
    yum install -y \
    gcc44 \
    gcc44-c++
fi

STACKBUILDER_HOME="/opt/stackbuilder"

echo "Making $STACKBUILDER_HOME"
sudo rm -rf $STACKBUILDER_HOME
sudo mkdir -p $STACKBUILDER_HOME
sudo chmod 777 $STACKBUILDER_HOME

echo "Running Stackbuilder to Install Stackbuilder"
python Stackbuilder.py -c app.yml -dvb

echo "Installing Stackbuilder Dependencies"
LDFLAGS=-Wl,-rpath,$STACKBUILDER_HOME/lib CFLAGS=-I$STACKBUILDER_HOME/include $STACKBUILDER_HOME/bin/pip install -r requirements.txt

echo "Assembling Stackbuilder Components"
mkdir $STACKBUILDER_HOME/lib/python2.7/site-packages/stackbuilder
cp -r * $STACKBUILDER_HOME/lib/python2.7/site-packages/stackbuilder

echo "Creating a convenience link in $STACKBUILDER_HOME/bin"
ln -s $STACKBUILDER_HOME/lib/python2.7/site-packages/stackbuilder/bin/stackbuilder $STACKBUILDER_HOME/bin/stackbuilder
ln -s $STACKBUILDER_HOME/lib/python2.7/site-packages/stackbuilder/bin/stackbuilder.sh $STACKBUILDER_HOME/bin/stackbuilder.sh

sudo chmod 755 $STACKBUILDER_HOME

echo "Creating Tarball"
tar czf stackbuilder-oel6-$BUILDNUMBER.tar.gz -C /opt stackbuilder