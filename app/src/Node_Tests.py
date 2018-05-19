class EqualityTest(unittest.TestCase):
    def testExpectEqual(self):
        self.assertEqual(1, 3 - 2)

    def testExpectNotEqual(self):
        self.assertNotEqual(2, 3 - 2)


class SimplisticTest(unittest.TestCase):
    # basic assert True test
    def testPass(self):
        x = True
        self.assertTrue(x)

    # basic assert False test
    def testFail(self):
        x = False
        self.assertFalse(x)

        # basic assert Equal

    def testEqual(self):
        x = 2
        self.assertEqual(x, 2)

    def testPass(self):
        return

    def test_doNothing(self):
        pass


class AlmostEqualTest(unittest.TestCase):
    # Not pass Equal 1.1 != 1.8999999999996
    # def testEqual(self):
    #    self.assertEqual(1.1, 3.3 - 2.2)

    def testAlmostEqual(self):
        self.assertAlmostEqual(1.1, 3.3 - 2.2, places=1)

    def testNotAlmostEqual(self):
        self.assertNotAlmostEqual(1.1, 3.3 - 2.0, places=1)


class UntitledCoinTest(unittest.TestCase):
    def testInstances(self):
        self.assertIsInstance(b, Block)

    def testEqualBlock(self):
        self.assertIs(b, b)

    def testEqualHashFromBlock(self):
        first_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0),
                            BlockPayload(t))
        secound_block = Block(BlockHeader(0, "May your spirit be always backed by enough firepower.", 00000000, 0, 0),
                              BlockPayload(t))
        hf = (hashlib.sha256(str(first_block).encode("utf-8"))).hexdigest()
        hf2 = (hashlib.sha256(str(secound_block).encode("utf-8"))).hexdigest()

        self.assertEqual(hf, hf2)
