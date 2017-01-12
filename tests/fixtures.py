import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from project.Project import Project
from component.Component import Component

def fargle():
    prj = Project()
    prj.name = 'fargle'
    prj.version = '1.2.3'

    prj.locations = {
    'rootdir': '/apps/fargle/tools',
    'libdir': '/apps/fargle/tools/lib',
    'docdir': '/apps/fargle/tools/doc',
    }

    pcreData = {
        'project': prj,
        'name': 'pcre',
        'version': '8.38',
        'src': {
            'type': 'tar.bz2',
            'url': 'http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.bz2'
        },
        'chk': {
            'type': 'gpg',
            'url': 'http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.bz2.sig'
        },
        'build': {
            'steps': [
                './configure --prefix=${libdir}/${name} --docdir=${docdir} --enable-unicode-properties --enable-pcre16 --enable-pcre32 --enable-pcregrep-libz --enable-pcregrep-libbz2 --enable-pcretest-libreadline --disable-static',
                'make',
                'make install',
            ]
        }
    }

    pcre = Component(pcreData)
    prj.components.append(pcre)

    httpdData = {
        'project': prj,
        'name': 'httpd',
        'version': '2.4.18',
        'src': {
            'type': 'tar.bz2',
            'url': 'https://archive.apache.org/dist/httpd/httpd-2.4.18.tar.bz2'
        },
        'chk': {
            'type': 'sha1',
            'url': 'https://archive.apache.org/dist/httpd/httpd-2.4.18.tar.bz2.sha1'
        },
        'build': {
            'steps': [
                'make distclean',
                './configure --prefix=${rootdir}/httpd-${version} --enable-so --enable-auth-digest --enable-rewrite --enable-setenvif --enable-mime --enable-deflate --enable-headers --with-pcre=${libdir}/pcre --with-included-apr',
                'make',
                'make install'
            ]
        }
    }

    httpd = Component(httpdData)
    prj.components.append(httpd)

    return prj


