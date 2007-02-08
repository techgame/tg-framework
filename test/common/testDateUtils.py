##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
import datetime
from TG.common import dateUtils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestDateUtils(unittest.TestCase):
    testItem = datetime.datetime(2005, 8, 18, 9, 20, 18, 112300)

    def testFromDateTime(self):
        self.assertEqual(dateUtils.datetimeFromISO(self.testItem.isoformat()), self.testItem)
        self.assertEqual(dateUtils.datetimeFromISO(self.testItem.isoformat('!')), self.testItem)
        self.assertEqual(dateUtils.dateFromISO(self.testItem.isoformat()), self.testItem.date())

    def testFromDate(self):
        testDate = self.testItem.date()
        self.assertEqual(dateUtils.dateFromISO(testDate.isoformat()), testDate)
        self.assertEqual(dateUtils.datetimeFromISO(testDate.isoformat()).timetuple(), testDate.timetuple())
        self.assertEqual(dateUtils.dateFromISO(self.testItem.isoformat()), testDate)
    
    def testFromTime(self):
        testTime = self.testItem.time()
        self.assertEqual(dateUtils.timeFromISO(testTime.isoformat()), testTime)
    
class TestTodayDateUtils(TestDateUtils):
    testItem = datetime.datetime.today()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

