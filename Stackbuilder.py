import yaml
import requests
import tempfile
import os
import hashlib
import gnupg
import re
import tarfile
import getopt
import sys
import zipfile
from subprocess import check_call, call, Popen
from project.Project import Project
from project.Prebuild import Prebuild
from component.Component import Component
from VerificationError import VerificationError
from UnknownSourceTypeError import UnknownSourceTypeError


class Stackbuilder:
    def __init__(self, buildspec, tempdir=None):
        # create work dir
        if tempdir is None:
            self.tempDir = tempfile.mkdtemp()
        else:
            self.tempDir = os.path.abspath(tempdir)

        # create work dir structure
        self.srcDir = self.tempDir + '/src'
        self.workDir = self.tempDir + '/work'
        self.gpgDir = self.tempDir + '/gpg'

        if not os.path.exists(self.srcDir):
            os.mkdir(self.srcDir)                                   # sources downloaded here

        if not os.path.exists(self.workDir):
            os.mkdir(self.workDir)                                  # actual work done here (configure, etc)

        if not os.path.exists(self.gpgDir):
            os.mkdir(self.gpgDir, 0700)                             # where gpg keys will be stored

        # parse buildspec create Component objects
        with open(buildspec, 'r') as stream:
            try:
                appyaml = yaml.load(stream)                         # load the full app.yaml
                self.config = appyaml.get('stack')
                self.gpgbinary = self.config.get('gpgbinary')       # pull just the 'stack' section.  The rest we ignore
                project = Project()
                project.name = appyaml.get('name')                  # name is the exception
                project.version = self.config.get('version')
                project.locations = self.config.get('locations')
                self.prebuild = Prebuild(project, appyaml.get('before_install'))

                for compData in self.config.get('components'):
                    compData['project'] = project                   # add the project to the data hash, as it's needed for variable interpolation
                    comp = Component(compData)
                    project.components.append(comp)

                self.project = project

            except yaml.YAMLError as exc:
                print exc

        # create install location tree
        for dirname in self.project.locations:
            # print "Creating Dir: "+ dirname
            if not os.path.exists(self.tempDir + os.sep + dirname):
                os.mkdir(self.tempDir + os.sep + dirname)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # loop through the components and pull down the source, checking the sigs and checksums
    def downloadComponents(self):
        for comp in self.project.components:
            name = comp.name

            if self.verbose:
                print "Downloading " + comp.src.url
            self.download(comp.src.url, self.srcDir)

            urlregex = re.compile(r'^(?:http|ftp)s?://', re.IGNORECASE)

            if comp.chk.url is not None and urlregex.match(comp.chk.url):
                if self.verbose:
                    print "Downloading " + comp.chk.url
                self.download(comp.chk.url, self.srcDir)

            srcFile = self.srcDir + os.sep + comp.src.filename
            chkFile = self.srcDir + os.sep + comp.chk.filename

            chkType = comp.chk.type

            if chkType == 'gpg':
                try:
                    gpg = gnupg.GPG(gnupghome=self.gpgDir, gpgbinary=self.gpgbinary, verbose=True)
                    gpg.encoding = 'utf-8'

                    if self.verbose:
                        print "Signature: " + comp.chk.key

                        print "Downloading key from keyserver.ubuntu.com"

                    if not gpg.recv_keys('keyserver.ubuntu.com', comp.chk.key):
                        raise VerificationError("Could not get key: "+comp.chk.key)

                    if self.verbose:
                        print "Verifying Signature"

                    with open(chkFile, "rb") as stream:
                        verified = gpg.verify_file(stream, srcFile)
                        print stream
                        print srcFile
                        if not verified: raise VerificationError("GPG Signature in " + comp.chk.filename + " failed to verify for: " + comp.src.filename)
                except TypeError:
                    print "GPG Verification not available with this OS.  Potentially unsafe, but continuing."

            elif chkType == 'sha1':
                if urlregex.match(comp.chk.url):
                    if self.verbose:
                        print "Verifying Checksum in downloaded file"

                    try:
                        expected, junk = open(chkFile, 'r').read().split(' ')
                        actual = self.sha1sum(srcFile)

                        if not expected == actual:
                            raise VerificationError("Component "+ name + " failed to verify.  Expected" + expected + " but got " + actual)
                    except ValueError:
                        expected = open(chkFile, 'r').read().rstrip()
                        actual = self.sha1sum(srcFile)

                        if not expected == actual:
                            raise VerificationError("Component "+ name + " failed to verify.  Expected" + expected + " but got " + actual)

                else:
                    if self.verbose:
                        print "Verifying Checksum from config yaml"

                    expected = comp.chk.url
                    actual = self.sha1sum(srcFile)

                    if not expected == actual:
                        raise VerificationError("Component "+ name + " failed to verify.  Expected" + expected + " but got " + actual)

            elif chkType == 'none':
                print "No check type is a bad idea, but I guess I'll go along with it"

            else:
                raise VerificationError("Unknown verification type: "+ chkType)

    def runPreBuildSteps(self):
        if self.verbose:
            print "********** Running Prebuild Steps **********"
        for cmd in self.prebuild.steps:
            if self.verbose:
                print "---------- PreBuild Command: " + cmd + " ----------"

            call(cmd, shell=True)

    def unpackAndBuildComponents(self):
        for comp in self.project.components:
            # unpack
            os.chdir(self.workDir)
            archive = self.srcDir + os.sep + comp.src.filename

            if self.verbose:
                print "********** Unpacking "+ archive + " **********"

            if bool(re.search('tar', comp.src.type) or re.search('tgz', comp.src.type)):
                tar = tarfile.open(archive)
                archiveDir =  tar.firstmember.name.split('/')[0]
                tar.extractall()
                tar.close()

                self.buildComponent(comp, archiveDir)

            elif bool(re.search('zip', comp.src.type)):
                zip = zipfile.ZipFile(archive)
                archiveDir = zip.infolist()[0].filename.split('/')[0]
                zip.extractall()
                zip.close

                self.buildComponent(comp, archiveDir)

            else:
                raise UnknownSourceTypeError("Unknown Source Type: " + str(comp.src.type))

    def buildComponent(self, comp, archiveDir) :
        # cd into build dir
        if self.verbose:
            print "Newly unpacked source dir: " + archiveDir

        os.chdir(archiveDir)

        # run commands
        if self.verbose:
            print "========== Building Component: " + comp.name + " =========="

        for cmd in comp.build.steps:
            if self.verbose:
                print "---------- Command: " + cmd + " ----------"

            call(cmd, shell=True)

    def download(self, src, dst):
        # grab the file name out of the url
        local_filename = src.split('/')[-1]
        if self.verbose:
            print "Downloading " + src + " to " + dst + os.sep + local_filename

        # make request
        r = requests.get(src, stream=True)

        # read it in chunks
        with open(dst + '/' + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    def sha1sum(self, filename, blocksize=65536):
        if self.verbose:
            print "Validating " + filename

        hash = hashlib.sha1()
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                hash.update(block)
        return hash.hexdigest()

    def verifySignature(self, expected, file, sig):
        if self.verbose:
            print "Validating signature of " + file

        if self.haveSignature(sig):
            return False
        else:
            return False

    def verbose(self, verbose):
        self.verbose = verbose

if __name__ == "__main__":
    config = None
    tempdir = None
    download = False
    build = False
    verbose = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:t:dbv',['config=','tempdir=','download', 'build','verbose'])

        for opt, arg in opts:
            if opt == '-h':
                print "Stackbuilder.py -c <config> [-db]\n" \
                      "-d download and verify files\n" \
                      "-b build components\n" \
                      "-t tempdir"
                sys.exit()
            elif opt in ("-c", "--config"):
                config = arg
            elif opt in ("-t", "--tempdir"):
                tempdir = arg
            elif opt in ("-d", "--download"):
                download = True
            elif opt in ("-b", "--build"):
                build = True
            elif opt in ("-v", "--verbose"):
                verbose = True

        if config is not None:
            sb = Stackbuilder(config, tempdir)
            sb.verbose(verbose)

            sb.runPreBuildSteps()

            if download:
                print "Downloading Components"
                sb.downloadComponents()

                if build:
                    print "Building Components"
                    sb.unpackAndBuildComponents()

        else:
            print "No config.  Can't continue."
    except getopt.GetoptError:
        print 'Stackbuilder.py -c <config> [-db]'
        sys.exit(2)

