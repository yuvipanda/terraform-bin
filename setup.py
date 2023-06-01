#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import http
import io
import os.path
import platform
import stat
import sys
import tarfile
import urllib.request
import zipfile

from distutils.command.build import build as orig_build
from distutils.core import Command
from setuptools import setup
from setuptools.command.install import install as orig_install

TERRAFORM_VERSION = '1.4.6'
POSTFIX_SHA256 = {
    ('linux', 'aarch64'): (
        '_linux_arm64.zip',
        'b38f5db944ac4942f11ceea465a91e365b0636febd9998c110fbbe95d61c3b26'
    ),
    ('linux', 'x86_64'): (
        '_linux_amd64.zip',
        'e079db1a8945e39b1f8ba4e513946b3ab9f32bd5a2bdf19b9b186d22c5a3d53b',
    ),
    ('darwin', 'x86_64'): (
        '_darwin_amd64.zip',
        '5d8332994b86411b049391d31ad1a0785dfb470db8b9c50617de28ddb5d1f25d',
    ),
    ('darwin', 'arm64'): (
        '_darwin_arm64.zip',
        '30a2f87298ff9f299452119bd14afaa8d5b000c572f62fa64baf432e35d9dec1',
    ),
    ('win32', 'AMD64'): (
        '_windows_amd64.zip',
        'f666aa1388f94c9b86ea01cb884ba53b9132d2cec3d9cac976ad93a2aba901d5',
    ),
}
POSTFIX_SHA256[('cygwin', 'x86_64')] = POSTFIX_SHA256[('win32', 'AMD64')]
PY_VERSION = '1'


def get_download_url() -> tuple[str, str]:
    postfix, sha256 = POSTFIX_SHA256[(sys.platform, platform.machine())]
    url = (
        f'https://releases.hashicorp.com/terraform/{TERRAFORM_VERSION}/terraform_{TERRAFORM_VERSION}{postfix}'
    )
    print(url)
    return url, sha256


def download(url: str, sha256: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        code = resp.getcode()
        if code != http.HTTPStatus.OK:
            raise ValueError(f'HTTP failure. Code: {code}')
        data = resp.read()

    checksum = hashlib.sha256(data).hexdigest()
    if checksum != sha256:
        raise ValueError(f'sha256 mismatch, expected {sha256}, got {checksum}')

    return data


def extract(url: str, data: bytes) -> bytes:
    with io.BytesIO(data) as bio:
        if url.endswith('.zip'):
            with zipfile.ZipFile(bio) as zipf:
                for info in zipf.infolist():
                    if info.filename.endswith('.exe') or info.filename.endswith('terraform'):
                        return zipf.read(info.filename)

    raise AssertionError(f'unreachable {url}')


def save_executable(data: bytes, base_dir: str):
    exe = 'terraform' if sys.platform != 'win32' else 'terraform.exe'
    output_path = os.path.join(base_dir, exe)
    os.makedirs(base_dir)

    with open(output_path, 'wb') as fp:
        fp.write(data)

    # Mark as executable.
    # https://stackoverflow.com/a/14105527
    mode = os.stat(output_path).st_mode
    mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    os.chmod(output_path, mode)


class build(orig_build):
    sub_commands = orig_build.sub_commands + [('fetch_binaries', None)]


class install(orig_install):
    sub_commands = orig_install.sub_commands + [('install_terraform', None)]


class fetch_binaries(Command):
    build_temp = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('build', ('build_temp', 'build_temp'))

    def run(self):
        # save binary to self.build_temp
        url, sha256 = get_download_url()
        archive = download(url, sha256)
        data = extract(url, archive)
        save_executable(data, self.build_temp)


class install_terraform(Command):
    description = 'install the terraform executable'
    outfiles = ()
    build_dir = install_dir = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        # this initializes attributes based on other commands' attributes
        self.set_undefined_options('build', ('build_temp', 'build_dir'))
        self.set_undefined_options(
            'install', ('install_scripts', 'install_dir'),
        )

    def run(self):
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)

    def get_outputs(self):
        return self.outfiles


command_overrides = {
    'install': install,
    'install_terraform': install_terraform,
    'build': build,
    'fetch_binaries': fetch_binaries,
}


try:
    from wheel.bdist_wheel import bdist_wheel as orig_bdist_wheel
except ImportError:
    pass
else:
    class bdist_wheel(orig_bdist_wheel):
        def finalize_options(self):
            orig_bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            _, _, plat = orig_bdist_wheel.get_tag(self)
            # We don't contain any python source, nor any python extensions
            return 'py2.py3', 'none', plat

    command_overrides['bdist_wheel'] = bdist_wheel

setup(version=f'{TERRAFORM_VERSION}.{PY_VERSION}', cmdclass=command_overrides)
