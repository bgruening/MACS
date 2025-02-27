#!/usr/bin/env python
# Time-stamp: <2025-02-15 08:23:55 Tao Liu>

import unittest

from MACS3.IO.Parser import (guess_parser,
                             BEDParser,
                             SAMParser,
                             BAMParser,
                             FragParser)


class Test_auto_guess(unittest.TestCase):

    def setUp(self):
        self.bedfile = "test/tiny.bed.gz"
        self.bedpefile = "test/tiny.bedpe.gz"
        self.samfile = "test/tiny.sam.gz"
        self.bamfile = "test/tiny.bam"

    def test_guess_parser_bed(self):
        p = guess_parser(self.bedfile)
        self.assertTrue(p.is_gzipped())
        self.assertTrue(isinstance(p, BEDParser))

    def test_guess_parser_sam(self):
        p = guess_parser(self.samfile)
        self.assertTrue(p.is_gzipped())
        self.assertTrue(isinstance(p, SAMParser))

    def test_guess_parser_bam(self):
        p = guess_parser(self.bamfile)
        self.assertTrue(p.is_gzipped())
        self.assertTrue(isinstance(p, BAMParser))


class Test_parsing(unittest.TestCase):
    def setUp(self):
        self.bedfile = "test/tiny.bed.gz"
        self.bedpefile = "test/tiny.bedpe.gz"
        self.samfile = "test/tiny.sam.gz"
        self.bamfile = "test/tiny.bam"
        self.fragfile = "test/test.fragments.tsv.gz"

    def test_fragment_file(self):
        p = FragParser(self.fragfile)
        petrack = p.build_petrack()
        petrack.finalize()
        bdg = petrack.pileup_bdg()
        bdg2 = petrack.pileup_bdg2()
        peaks = bdg.call_peaks(cutoff=10, min_length=200, max_gap=100)
        peaks2 = bdg2.call_peaks(cutoff=10, min_length=200, max_gap=100)
        # print(peaks)
        # print(peaks2)
