#!/usr/bin/env python
# Time-stamp: <2025-02-12 13:44:51 Tao Liu>

import unittest
from MACS3.Signal.PairedEndTrack import PETrackI, PETrackII
from MACS3.Signal.Region import Regions
import numpy as np


class Test_PETrackI(unittest.TestCase):
    def setUp(self):
        self.input_regions = [(b"chrY", 0, 100),  # 17 tags in chrY
                              (b"chrY", 70, 270),  # will exclude
                              (b"chrY", 70, 100),  # will exclude
                              (b"chrY", 80, 160),  # will exclude
                              (b"chrY", 80, 160),  # will exclude
                              (b"chrY", 80, 180),  # will exclude
                              (b"chrY", 80, 180),  # will exclude
                              (b"chrY", 85, 185),  # will exclude
                              (b"chrY", 85, 285),  # will exclude
                              (b"chrY", 85, 285),  # will exclude
                              (b"chrY", 85, 285),  # will exclude
                              (b"chrY", 85, 385),  # will exclude
                              (b"chrY", 90, 190),  # will exclude
                              (b"chrY", 90, 190),  # will exclude
                              (b"chrY", 90, 191),  # will exclude
                              (b"chrY", 150, 190),  # will exclude
                              (b"chrY", 150, 250),  # will exclude
                              (b"chrX", 0, 100),  # 9 tags in chrX
                              (b"chrX", 70, 270),  # will exclude
                              (b"chrX", 70, 100),  # will exclude
                              (b"chrX", 80, 160),
                              (b"chrX", 80, 180),
                              (b"chrX", 85, 185),
                              (b"chrX", 85, 285),
                              (b"chrX", 90, 190),
                              (b"chrX", 90, 191)
                              ]
        self.t = sum([x[2]-x[1] for x in self.input_regions])

        self.exclude_regions = [(b"chrY", 85, 200), (b"chrX", 50, 75)]
        self.x_regions = Regions()
        for r in self.exclude_regions:
            self.x_regions.add_loc(r[0], r[1], r[2])

        self.pe = PETrackI()
        for (c, l, r) in self.input_regions:
            self.pe.add_loc(c, l, r)
        self.pe.finalize()

    def test_add_loc(self):
        self.assertEqual(self.pe.total, 26)
        self.assertEqual(self.pe.length, self.t)

    def test_filter_dup(self):
        self.pe.filter_dup(3)
        self.assertEqual(self.pe.total, 26)

        self.pe.filter_dup(2)
        self.assertEqual(self.pe.total, 25)

        self.pe.filter_dup(1)
        self.assertEqual(self.pe.total, 21)

    def test_sample_num(self):
        self.pe.sample_num(10)  # percentage is 38.5%
        self.assertEqual(self.pe.total, 9)

    def test_sample_percent(self):
        self.pe.sample_percent(0.5)  # 12=int(0.5*17)+int(0.5*9)
        self.assertEqual(self.pe.total, 12)

    def test_pileupbdg(self):
        self.pe.pileup_bdg()

    def test_exclude(self):
        self.pe.exclude(self.x_regions)
        self.assertEqual(self.pe.total, 7)
        self.assertEqual(self.pe.length, 781)
        self.assertAlmostEqual(self.pe.average_template_length, 112, 0)


class Test_PETrackII(unittest.TestCase):
    def setUp(self):
        self.input_regions = [(b"chrY", 0, 100, b"0w#AAACGAAAGACTCGGA", 2),  # will be excluded
                              (b"chrY", 70, 170, b"0w#AAACGAAAGACTCGGA", 1),  # will be excluded
                              (b"chrY", 80, 190, b"0w#AAACGAAAGACTCGGA", 1),
                              (b"chrY", 85, 180, b"0w#AAACGAAAGACTCGGA", 3),
                              (b"chrY", 100, 190, b"0w#AAACGAAAGACTCGGA", 1),
                              (b"chrY", 0, 100, b"0w#AAACGAACAAGTAACA", 1),  # will be excluded
                              (b"chrY", 70, 170, b"0w#AAACGAACAAGTAACA", 2),  # will be excluded
                              (b"chrY", 80, 190, b"0w#AAACGAACAAGTAACA", 1),
                              (b"chrY", 85, 180, b"0w#AAACGAACAAGTAACA", 1),
                              (b"chrY", 100, 190, b"0w#AAACGAACAAGTAACA", 3),
                              (b"chrY", 10, 110, b"0w#AAACGAACAAGTAAGA", 1),  # will be excluded
                              (b"chrY", 50, 160, b"0w#AAACGAACAAGTAAGA", 2),  # will be excluded
                              (b"chrY", 100, 170, b"0w#AAACGAACAAGTAAGA", 3)
                              ]

        self.exclude_regions = [(b"chrY", 10, 75)]
        self.x_regions = Regions()
        for r in self.exclude_regions:
            self.x_regions.add_loc(r[0], r[1], r[2])

        self.pileup_p = np.array([10, 50, 70, 80, 85,
                                  100, 110, 160, 170, 180,
                                  190], dtype="i4")
        self.pileup_v = np.array([3.0, 4.0, 6.0, 9.0, 11.0,
                                  15.0, 19.0, 18.0, 16.0, 10.0,
                                  6.0], dtype="f4")
        self.peak_str = "chrom:chrY	start:80	end:180	name:peak_1	score:19	summit:105\n"
        self.subset_barcodes = {b'0w#AAACGAACAAGTAACA', b"0w#AAACGAACAAGTAAGA"}
        self.subset_pileup_p = np.array([10, 50, 70, 80, 85,
                                         100, 110, 160, 170, 180,
                                         190], dtype="i4")
        self.subset_pileup_v = np.array([1.0, 2.0, 4.0, 6.0, 7.0,
                                         8.0, 13.0, 12.0, 10.0, 5.0,
                                         4.0], dtype="f4")
        self.subset_peak_str = "chrom:chrY	start:100	end:170	name:peak_1	score:13	summit:105\n"
        self.t = sum([(x[2]-x[1]) * x[4] for x in self.input_regions])

        self.pe = PETrackII()
        for (c, l, r, b, C) in self.input_regions:
            self.pe.add_loc(c, l, r, b, C)
        self.pe.finalize()

    def test_add_frag(self):
        self.assertEqual(self.pe.total, 22)
        self.assertEqual(self.pe.length, self.t)

        pe_subset = self.pe.subset(self.subset_barcodes)
        self.assertEqual(pe_subset.total, 14)
        self.assertEqual(pe_subset.length, 1305)

    def test_pileup(self):
        bdg = self.pe.pileup_bdg()
        d = bdg.get_data_by_chr(b'chrY')
        np.testing.assert_array_equal(d[0], self.pileup_p)
        np.testing.assert_array_equal(d[1], self.pileup_v)

        pe_subset = self.pe.subset(self.subset_barcodes)
        bdg = pe_subset.pileup_bdg()
        d = bdg.get_data_by_chr(b'chrY')
        np.testing.assert_array_equal(d[0], self.subset_pileup_p)
        np.testing.assert_array_equal(d[1], self.subset_pileup_v)

    def test_pileup2(self):
        bdg = self.pe.pileup_bdg2()
        d = bdg.get_data_by_chr(b'chrY')
        np.testing.assert_array_equal(d['p'], self.pileup_p)
        np.testing.assert_array_equal(d['v'], self.pileup_v)

        pe_subset = self.pe.subset(self.subset_barcodes)
        bdg = pe_subset.pileup_bdg2()
        d = bdg.get_data_by_chr(b'chrY')
        np.testing.assert_array_equal(d['p'], self.subset_pileup_p)
        np.testing.assert_array_equal(d['v'], self.subset_pileup_v)

    def test_callpeak(self):
        bdg = self.pe.pileup_bdg()
        peaks = bdg.call_peaks(cutoff=10, min_length=20, max_gap=10)
        self.assertEqual(str(peaks), self.peak_str)

        pe_subset = self.pe.subset(self.subset_barcodes)
        bdg = pe_subset.pileup_bdg()
        peaks = bdg.call_peaks(cutoff=10, min_length=20, max_gap=10)
        self.assertEqual(str(peaks), self.subset_peak_str)

    def test_callpeak2(self):
        bdg = self.pe.pileup_bdg2()
        peaks = bdg.call_peaks(cutoff=10, min_length=20, max_gap=10)
        self.assertEqual(str(peaks), self.peak_str)

        pe_subset = self.pe.subset(self.subset_barcodes)
        bdg = pe_subset.pileup_bdg2()
        peaks = bdg.call_peaks(cutoff=10, min_length=20, max_gap=10)
        self.assertEqual(str(peaks), self.subset_peak_str)

    def test_exclude(self):
        self.pe.exclude(self.x_regions)
        self.assertEqual(self.pe.total, 13)
        self.assertEqual(self.pe.length, 1170)
        self.assertAlmostEqual(self.pe.average_template_length, 90, 0)
