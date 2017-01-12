# Stackbuilder

Stackbuilder is a tool to build stacks of software from multiple sources.

## Build Status: [![CircleCI](https://circleci.com/gh/nikogura/stackbuilder.svg?style=svg)](https://circleci.com/gh/nikogura/stackbuilder)

## Why?

If you've ever built an application stack, you'll know that there are all sorts of ways to get the pieces on a box, and lots of ways you can link them together.

If you're really lucky you have up to date packages from your distribution and can just 'yum update', or 'apt-get update', and everthing is magically there, all upgraded to the latest version, with all the latest patches, and it all just works together tra la la.

For the rest of us there's Stackmaker, a framework that allows you to specify what your components are, where they come from, and how to build them to make a complete working stack, and reproduce/ rebuild it on demand when a component needs updating or you need something almost like it, but slightly different.

## Usage

    stackbuilder -c /path/to/stack.yml -dvb 
    
## Example stack.yml

    name: stackbuilder
    stack:
      version: 0.1.0
      locations:
        rootdir: /opt/stackbuilder
        libdir: /opt/stackbuilder/lib
        includedir: /opt/stackbuilder/lib
      gpgbinary: /usr/bin/gpg
      components:
        - name: openssl
          version: 1.0.2g
          src:
            type: tar.gz
            url: https://www.openssl.org/source/openssl-1.0.2h.tar.gz
          chk:
            type: sha1
            url: https://www.openssl.org/source/openssl-1.0.2h.tar.gz.sha1
            key:
          build:
            steps:
              - ./config --prefix=${rootdir} --shared
              - make
              - make test
              - make install

        - name: tcl
          version: 8.6.5
          src:
            type: tar.gz
            url: http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz
          chk:
            type: none
            url:
          build:
            steps:
              - cd unix && LDFLAGS=-Wl,-rpath,${libdir} ./configure --prefix=${rootdir}
              - cd unix && make
              - cd unix && make test
              - cd unix && make install

        - name: sqlite
          version: 3130000
          src:
            type: zip
            url: https://www.sqlite.org/2016/sqlite-src-3130000.zip
          chk:
            type: sha1
            url: e8a1530a0f2bfe427c966da5399f4d431ae51533
          build:
            steps:
              - chmod 755 configure
              - export PATH=${bindir}:$PATH && LDFLAGS=-Wl,-rpath,${libdir} ./configure --prefix=${rootdir} --with-tcl=${libdir}
              - make
              - make test
              - make install

        - name: python
          version: 2.7.11
          src:
            type: tgz
            url: http://www.python.org/ftp/python/2.7.11/Python-${version}.tgz
          chk:
            type: gpg
            url: http://www.python.org/ftp/python/2.7.11/Python-${version}.tgz.asc
            key: 18ADD4FF
          build:
            steps:
              - LDFLAGS=-Wl,-rpath,${libdir} CPPFLAGS=-I${includedir} ./configure --prefix=${rootdir} --enable-unicode=ucs2 --enable-shared --with-ensurepip=install
              - make
              - make install
