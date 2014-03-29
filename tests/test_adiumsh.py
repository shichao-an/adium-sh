from unittest import TestCase
from scripttest import TestFileEnvironment
import shlex
import time
from adiumsh import adiumsh
from adiumsh.utils import get_process
from .secret import TEST_ACCOUNT, TEST_SERVICE, TEST_ALIAS


class TestAdiumsh(TestCase):

    @classmethod
    def setUpClass(cls):
        proc = get_process('Adium')
        if proc:
            proc.terminate()
        time.sleep(1)

        cls.adium = adiumsh.Adium(account=TEST_ACCOUNT,
                                  service=TEST_SERVICE)

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

    def setUp(self):
        self.env = TestFileEnvironment('./test-output')

    def test_send_no_args(self):
        cmd = 'python ../run.py send'
        self.env.run(*shlex.split(cmd), expect_error=True)
