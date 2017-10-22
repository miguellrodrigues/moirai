#!/usr/bin/env python3
# -*- coding: utf-8; -*-
#
# Copyright (c) 2016 Álan Crístoffer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import glob
import os
import platform
import shutil
import sys
import zipfile

from urllib.request import urlopen

opt = os.path.join(os.path.abspath(os.sep), 'opt')


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def download_snap7_linux():
    arch = {
        'x64': 'x86_64',
        'ia32': 'i386',
        'x86': 'i386',
        'armv7': 'arm_v7',
        'armv6': 'arm_v6'
    }.get(platform.machine(), platform.machine())
    print('Downloading snap7...')
    try:
        if not os.path.exists('snap7.zip'):
            snap7url = 'https://sourceforge.net/projects/snap7/files/1.4.2/snap7-full-1.4.2.7z/download'
            contents = urlopen(snap7url).read()
            with open('snap7.zip', 'wb') as f:
                f.write(contents)
        os.system('7z x -y snap7.zip')
        with cd('snap7-full-1.4.2/build/unix'):
            os.system(f'make -f {arch}_linux.mk')
        lib = f'snap7-full-1.4.2/build/bin/{arch}-linux/libsnap7.so'
        shutil.copy(lib, os.path.join(opt, 'libsnap7.so'))
        os.chmod(os.path.join(opt, 'libsnap7.so'), 0o777)
        os.remove('snap7.zip')
        shutil.rmtree('snap7-full-1.4.2')
        return True
    except:
        return False


def download_snap7_win():
    print('Downloading snap7...')
    try:
        snap7url = 'https://sourceforge.net/projects/snap7/files/latest/download?source=files'
        contents = urlopen(snap7url).read()
        with open('snap7.zip', 'wb') as f:
            f.write(contents)
        with zipfile.ZipFile('snap7.zip', 'r') as zip_ref:
            zip_ref.extractall('snap7')
        dll = list(glob.iglob('snap7/**/*.dll'))[0]
        shutil.copy(dll, os.path.join(opt, 'snap7.dll'))
        os.remove('snap7.zip')
        shutil.rmtree('snap7')
        return True
    except:
        return False


def install():
    osname = platform.system()
    if osname == 'Windows':
        print('You need to install MongoDB.')
        print('https://www.mongodb.com')
        print('')
    elif osname == 'Darwin':
        brew = os.popen('which brew').read()
        if len(brew) > 0:
            print('Using Homebrew to install dependencies.')
            print('Will now execute: [brew install mongodb snap7]')
            result = os.system('brew install mongodb snap7')
            if result == 0:
                print('Installation finished.')
            else:
                print('Something went wrong. Try installing manually:')
                print('brew install mongodb snap7')
        else:
            print('Homebrew not installed, cannot continue alone.')
            print('You need to install MongoDB and snap7.')
            print('https://www.mongodb.com')
            print('https://sourceforge.net/projects/snap7/files')
    elif osname == 'Linux':
        distribution = platform.linux_distribution()[0]
        success = False
        if len(distribution) > 0:
            if len(os.popen('which apt-get').read()) > 0:
                cmd = 'apt-get install -y mongodb-server build-essential p7zip-full'
                print('Using APT to install dependencies.')
                print(f'Will now execute: [{cmd}]')
                result = os.system(cmd)
                if result == 0:
                    if download_snap7_linux():
                        print('Installation finished.')
                    else:
                        print('Something went wrong. Try installing manually:')
                        print('https://sourceforge.net/projects/snap7/files')
                else:
                    print('Something went wrong. Try installing manually:')
                    print(cmd)
                    print('After that, you need to install snap7.')
                    print('https://sourceforge.net/projects/snap7/files')
            elif len(os.popen('which dnf').read()) > 0:
                cmd = 'dnf install -y @development-tools p7zip mongodb-server'
                print('Using DNF to install dependencies.')
                print(f'Will now execute: [{cmd}]')
                result = os.system(cmd)
                if result == 0:
                    if download_snap7_linux():
                        print('Installation finished.')
                    else:
                        print('Something went wrong. Try installing manually:')
                        print('https://sourceforge.net/projects/snap7/files')
                else:
                    print('Something went wrong. Try installing manually:')
                    print(cmd)
                    print('After that, you need to install snap7.')
                    print('https://sourceforge.net/projects/snap7/files')
            elif len(os.popen('which yum').read()) > 0:
                cmd1 = 'yum groupinstall -y "Development Tools" "Development Libraries"'
                cmd2 = 'yum install -y p7zip mongodb-server'
                print('Using YUM to install dependencies.')
                print(f'Will now execute: [{cmd1}]')
                result1 = os.system(cmd1)
                print(f'Will now execute: [{cmd2}]')
                result2 = os.system(cmd2)
                if result1 == 0 and result2 == 0:
                    if download_snap7_linux():
                        print('Installation finished.')
                    else:
                        print('Something went wrong. Try installing manually:')
                        print('https://sourceforge.net/projects/snap7/files')
                else:
                    print('Something went wrong. Try installing manually:')
                    print(cmd1)
                    print(cmd2)
                    print('After that, you need to install snap7.')
                    print('https://sourceforge.net/projects/snap7/files')
            elif len(os.popen('which zypper').read()) > 0:
                cmd1 = 'zypper in -t devel_basis'
                cmd2 = 'zypper in mongodb p7zip'
                print('Using Zypper to install dependencies.')
                print(f'Will now execute: [{cmd1}]')
                result1 = os.system(cmd1)
                print(f'Will now execute: [{cmd2}]')
                result2 = os.system(cmd2)
                if result1 == 0 and result2 == 0:
                    if download_snap7_linux():
                        print('Installation finished.')
                    else:
                        print('Something went wrong. Try installing manually:')
                        print('https://sourceforge.net/projects/snap7/files')
                else:
                    print('Something went wrong. Try installing manually:')
                    print(cmd1)
                    print(cmd2)
                    print('After that, you need to install snap7.')
                    print('https://sourceforge.net/projects/snap7/files')
    else:
        print('Trying to install MongoDB and snap7...')
        if download_snap7_win():
            print('Downloading MongoDB...')
            mongo = 'https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.4.9-signed.msi'
            contents = urlopen(mongo).read()
            with open('mongo.msi', 'wb') as f:
                f.write(contents)
            result = os.system(
                r'msiexec.exe /q /i mongo.msi INSTALLLOCATION="C:\Program Files\MongoDB\Server\3.4.9\" ADDLOCAL="all"')
            if result:
                print('Installation finished.')
            else:
                print('You need to install MongoDB.')
                print('https://www.mongodb.com')
        else:
            print('You need to install MongoDB and snap7.')
            print('https://www.mongodb.com')
            print('https://sourceforge.net/projects/snap7/files')
