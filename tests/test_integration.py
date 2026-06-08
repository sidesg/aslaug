from __future__ import print_function, unicode_literals

import os
import shutil
import tempfile
import unittest

from src.aslaug import Analyser

def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

class SelfCleaningTestCase(unittest.TestCase):
    """TestCase subclass which cleans up self.tmpdir after each test"""

    def setUp(self):
        super(SelfCleaningTestCase, self).setUp()

        # tempdir for brunnhilde outputs
        self.dest_tmpdir = tempfile.mkdtemp()
        if not os.path.isdir(self.dest_tmpdir):
            os.mkdirs(self.dest_tmpdir)

        self.TEST_REPORT_DIR = os.path.join(self.dest_tmpdir, "test")

    def tearDown(self):
        if os.path.isdir(self.dest_tmpdir):
            shutil.rmtree(self.dest_tmpdir)

        super(SelfCleaningTestCase, self).tearDown()

class TestRunSf(SelfCleaningTestCase):
    def test_sf_output(self):
        os.makedirs(self.TEST_REPORT_DIR)

        analyser = Analyser.new(
            "./tests/test-data/files/",
            self.TEST_REPORT_DIR
        )
        analyser.run_siegfried()

        self.assertTrue(is_non_zero_file(analyser.sf_file))

class TestOverwriteReportDir(SelfCleaningTestCase):
    def test_overwrite_true(self):
        os.makedirs(self.TEST_REPORT_DIR)

        analyser = Analyser.new(
            "./tests/test-data/files/",
            self.TEST_REPORT_DIR,
            overwrite=True
        )
        analyser.create_report_dir()
        self.assertTrue(os.path.exists(analyser.report_dir))

    def test_overwrite_false(self):
        os.makedirs(self.TEST_REPORT_DIR)

        analyser = Analyser.new(
            "./tests/test-data/files/",
            self.TEST_REPORT_DIR
        )
        with self.assertRaises(FileExistsError):
            analyser.create_report_dir()
