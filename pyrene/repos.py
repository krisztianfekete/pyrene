# Py3 compatibility
from __future__ import print_function
from __future__ import unicode_literals

import abc
import os
import shutil
from upload import upload
from .util import pip_install, PyPI
from .constants import REPO, REPOTYPE


class Repo(object):
    __metaclass__ = abc.ABCMeta

    ATTRIBUTES = {REPO.TYPE}
    DEFAULT_ATTRIBUTES = dict()

    def __init__(self, attributes):
        super(Repo, self).__init__()
        self._attributes = dict(self.DEFAULT_ATTRIBUTES)
        self._attributes.update(attributes)

    def __getattr__(self, key):
        try:
            return self._attributes[key]
        except KeyError:
            raise AttributeError(key)

    @abc.abstractmethod
    def get_as_pip_conf(self):
        pass

    @abc.abstractmethod
    def download_packages(self, package_spec, directory):
        pass

    @abc.abstractmethod
    def upload_packages(self, package_files):
        pass

    @abc.abstractmethod
    def serve(self):
        pass


PIPCONF_NULLREPO = '''\
[global]
no-index = true
'''


class NullRepo(Repo):

    def get_as_pip_conf(self):
        return PIPCONF_NULLREPO

    def download_packages(self, package_spec, directory):
        print('NullRepo provided packages {}'.format(package_spec))

    def upload_packages(self, package_files):
        print('NullRepo swallowed packages {}'.format(' '.join(package_files)))

    def serve(self):
        print('NullRepo is not served')


PIPCONF_DIRECTORYREPO = '''\
[global]
no-index = true
find-links = {directory}
'''


class DirectoryRepo(Repo):

    ATTRIBUTES = {
        REPO.TYPE,
        REPO.DIRECTORY,
        REPO.VOLATILE,
        REPO.SERVE_INTERFACE,
        REPO.SERVE_PORT,
        REPO.SERVE_USERNAME,
        REPO.SERVE_PASSWORD,
    }

    DEFAULT_ATTRIBUTES = {
        REPO.TYPE: REPOTYPE.DIRECTORY,
        REPO.DIRECTORY: os.path.abspath('.'),
    }

    def get_as_pip_conf(self):
        return PIPCONF_DIRECTORYREPO.format(directory=self.directory)

    def download_packages(self, package_spec, directory):
        pip_install(
            '--find-links', self.directory,
            '--no-index',
            '--download', directory.path,
            package_spec,
        )

    def upload_packages(self, package_files):
        destination = self.directory
        for source in package_files:
            shutil.copy2(source, destination)

    def serve(self, pypi_server=PyPI):
        server = pypi_server()
        server.directory = self.directory
        server.interface = getattr(self, REPO.SERVE_INTERFACE, '0.0.0.0')
        server.port = getattr(self, REPO.SERVE_PORT, '8080')
        true = {'y', 'yes', 't', 'true'}
        server.volatile = getattr(self, REPO.VOLATILE, 'no').lower() in true

        try:
            username = getattr(self, REPO.SERVE_USERNAME)
            password = getattr(self, REPO.SERVE_PASSWORD)
        except AttributeError:
            pass
        else:
            server.add_user(username, password)

        server.serve()


PIPCONF_HTTPREPO = '''\
[global]
index-url = {download_url}
extra-index-url =
'''


class HttpRepo(Repo):

    ATTRIBUTES = {
        REPO.TYPE,
        REPO.UPLOAD_URL,
        REPO.DOWNLOAD_URL,
        REPO.USERNAME,
        REPO.PASSWORD,
    }

    DEFAULT_ATTRIBUTES = {
        REPO.DOWNLOAD_URL: 'http://localhost:8080/simple',
    }

    def get_as_pip_conf(self):
        return PIPCONF_HTTPREPO.format(download_url=self.download_url)

    def download_packages(self, package_spec, directory):
        pip_install(
            '--index-url', self.download_url,
            '--download', directory.path,
            package_spec,
        )

    def upload_packages(self, package_files):
        for source in package_files:
            upload(
                source,
                signature=None,
                repository=self.upload_url,
                username=self.username,
                password=self.password,
                comment='Uploaded with Pyrene',
            )

    def serve(self):
        print('Externally served at url {}'.format(self.download_url))
