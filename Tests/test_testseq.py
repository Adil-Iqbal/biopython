# Copyright 2017 by Adil Iqbal.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

import os
import unittest

from Bio.Alphabet import IUPAC, NucleotideAlphabet
from Bio.SeqUtils import GC


def manually_import(name):
    """Find, import, and return a module in Python 2.7."""
    name = name.split(".")
    name[-1] += ".py"
    module_path = os.getcwd()
    module_path = os.path.split(module_path)
    if module_path[1] == "Tests":
        module_path = os.path.join(module_path[0], name.pop(0))
    else:
        raise ImportError("Must call 'manually_import' from inside 'Tests' folder.")
    for i, step in enumerate(name):
        module_path = os.path.join(module_path, step)
    name = name[-1][:-3]
    import imp
    return imp.load_source(name, module_path)


try:
    import Scripts.testseq as module
except ImportError:
    module = manually_import("Scripts.testseq")


class TestTestseq(unittest.TestCase):
    """Perform unit test for 'testseq' function."""

    def test_alphabet(self):
        """Testing 'alphabet' argument..."""
        alphabets = [IUPAC.unambiguous_dna, IUPAC.ambiguous_dna, IUPAC.extended_dna,
                     IUPAC.unambiguous_rna, IUPAC.ambiguous_rna, IUPAC.protein, IUPAC.extended_protein]

        for i in alphabets:
            seq = module.testseq(alphabet=i)._data
            seq = seq[10:20]
            for j, letter in enumerate(seq):
                self.assertTrue(letter in i.letters)

        with self.assertRaises(TypeError):
            module.testseq(alphabet=NucleotideAlphabet)

    def test_size(self):
        """Testing 'size' and 'truncate' arguments..."""
        seq = module.testseq()
        self.assertEqual(len(seq), 30)

        seq = module.testseq(100)
        self.assertEqual(len(seq), 99)

        seq = module.testseq(100, alphabet=IUPAC.protein)
        self.assertEqual(len(seq), 100)

        seq = module.testseq(100, truncate=False)
        self.assertEqual(len(seq), 100)

    def test_gc_target(self):
        """Testing 'gc_target' argument..."""
        seq = module.testseq(1000, gc_target=90)
        error = 90 - GC(seq)
        self.assertTrue(-5 < error < 5)

    def test_codon_tables(self):
        """Testing codon sets..."""
        seq = module.testseq(table=5)
        seq1 = seq.translate(table=5)._data
        seq2 = seq.translate(table=6)._data

        self.assertTrue(seq1[0] == "M")
        self.assertFalse("*" in seq1[1:-1])
        self.assertTrue(seq1[-1] == "*")
        self.assertFalse(seq2[-1] == "*")

        seq = module.testseq(size=1000, from_start=False, to_stop=False, persistent=False)
        seq = seq.translate()._data

        self.assertFalse(seq[0] == "M")
        self.assertFalse(seq[-1] == "*")
        self.assertTrue("*" in seq[1:-1])

    def test_messenger(self):
        """Testing 'messenger' argument..."""
        seq = module.testseq(alphabet=IUPAC.unambiguous_rna, messenger=True)._data
        self.assertTrue("A" * 20 == seq[-20:])

    def test_seeding(self):
        """Testing 'rand_seed' argument..."""
        seq1 = module.testseq(rand_seed=None)
        seq2 = module.testseq(rand_seed=None)
        self.assertFalse(seq1 == seq2)

        seq1 = module.testseq(rand_seed=50)
        seq2 = module.testseq(rand_seed=50)
        self.assertTrue(seq1 == seq2)


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
