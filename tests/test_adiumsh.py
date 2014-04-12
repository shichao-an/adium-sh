import os
from unittest import TestCase
from scripttest import TestFileEnvironment
import shlex
import stat
import time
from adiumsh import adiumsh
from adiumsh.utils import get_process
from adiumsh.settings import REPO_PATH
from .secret import TEST_ACCOUNT, TEST_SERVICE, TEST_ALIAS


def create_run_script():
    run_script = os.path.join(REPO_PATH, 'run.py')
    content = '#!/usr/bin/env python\n'
    content += 'from adiumsh.adiumsh import main\n\n\n'
    content += 'main()'
    if not os.path.exists(run_script):
        create_executable(run_script, content)


def create_executable(path, content):
    with open(path, 'w') as f:
        f.write(content)
    s = os.stat(path)
    os.chmod(path, s.st_mode | stat.S_IEXEC)


class TestAdiumsh(TestCase):

    @classmethod
    def setUpClass(cls):
        proc = get_process('Adium')
        if proc:
            proc.terminate()
        time.sleep(1)
        cls.adium = adiumsh.Adium(account=TEST_ACCOUNT,
                                  service=TEST_SERVICE)
        time.sleep(1)

    def test_send_alias(self):
        self.adium.send_alias('Hi', TEST_ALIAS)

    def test_get_name(self):
        args = [TEST_SERVICE, TEST_ACCOUNT, TEST_ALIAS]
        res = self.adium.call_script('name', args)
        self.assertEqual(self.adium.get_name(TEST_ALIAS), res.strip())

    def test_send(self):
        name = self.adium.get_name(TEST_ALIAS)
        self.adium.send('Hi', name)

    @classmethod
    def tearDownClass(cls):
        proc = get_process('Adium')
        if proc:
            proc.terminate()


class TestCommands(TestCase):

    @classmethod
    def setUpClass(cls):
        create_run_script()

    def setUp(self):
        self.env = TestFileEnvironment('./test-output')

    def test_send_no_args(self):
        cmd = 'python ../run.py send'
        self.env.run(*shlex.split(cmd), expect_error=True)

    def test_send_alias_stdin(self):
        cmd = 'python ../run.py send -a "%s"' % (TEST_ALIAS)
        self.env.run(*shlex.split(cmd), stdin=b'Hi')
