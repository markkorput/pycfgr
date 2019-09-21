from unittest import TestCase

from cfgr.app import main

class TestApp(TestCase):
  def test_main_result(self):
    result = main()
    self.assertTrue(result == 'done')