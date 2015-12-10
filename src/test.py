#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Python CLI Test Unit
"""

# Standard library imports
import datetime
import os

# Third party imports

# Application specific imports
import jot

if (__name__ == "__main__"):
    
    # Basic unit tests for API()
    import unittest
    
    class APITestCase(unittest.TestCase):
        
        def setUp(self):
            self.api = jot.Jot()
            
        def tearDown(self):
            self.api = None
            try:
                os.remove("jot.txt")
            except:
                pass
            
        def testBasic(self):
            # Verify that the instance was created
            self.assertNotEqual(self.api, None)
            
        def testExecute(self):
            # Verify that the main execution routine returns True
            self.assertEqual(self.api.execute({"<date>": "2015-12-10", "<entry>": "Execute test"}), True)
            
        def test_adjust_date(self):
            # Verify that adjust_date() works in the simplest version
            today = datetime.datetime.now()
            self.assertEqual(self.api.adjust_date(today, ''), today)
                       
        def test_adjust_date_today(self):
            # Verify that adjust_date() returns the correct value 
            # for 'today'
            today = datetime.datetime.now()
            self.assertEqual(self.api.adjust_date(today, 'today'), today)
            
        def test_adjust_date_yesterday(self):
            # Verify that adjust_date() returns the correct value 
            # for 'yesterday'
            today = datetime.datetime.now()
            yesterday = today - datetime.timedelta(1)
            self.assertEqual(self.api.adjust_date(today, 'yesterday'), yesterday)

        def test_adjust_date_this_week(self):
            # Verify that adjust_date() returns the correct value 
            # for 'this-week'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            this_week = datetime.datetime.strptime("2015-07-20", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'this-week'), this_week)
            
        def test_adjust_date_this_month(self):
            # Verify that adjust_date() returns the correct value 
            # for 'this-month'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            this_month = datetime.datetime.strptime("2015-07-01", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'this-month'), this_month)
            
        def test_adjust_date_this_year(self):
            # Verify that adjust_date() returns the correct value 
            # for 'this-year'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            this_year = datetime.datetime.strptime("2015-01-01", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'this-year'), this_year)
            
        def test_adjust_date_last_week(self):
            # Verify that adjust_date() returns the correct value 
            # for 'last-week'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            last_week = datetime.datetime.strptime("2015-07-16", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'last-week'), last_week)
            
        def test_adjust_date_last_month(self):
            # Verify that adjust_date() returns the correct value 
            # for 'last-month'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            last_month = datetime.datetime.strptime("2015-06-23", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'last-month'), last_month)
            
        def test_adjust_date_last_month_for_february(self):
            # Verify that adjust_date() returns the correct value 
            # for 'last-month' when we are at the end of March and the day
            # would not be valid for February
            today = datetime.datetime.strptime("2015-03-30", "%Y-%m-%d")
            last_month = datetime.datetime.strptime("2015-02-28", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'last-month'), last_month)
            
        def test_adjust_date_last_month_across_year(self):
            # Verify that adjust_date() returns the correct value 
            # for 'last-month' when last month is in the previous year
            today = datetime.datetime.strptime("2015-01-18", "%Y-%m-%d")
            last_month = datetime.datetime.strptime("2014-12-18", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'last-month'), last_month)
            
        def test_adjust_date_day_nn(self):
            # Verify that adjust_date() returns the correct value 
            # for 'day-nn'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            day_nn = datetime.datetime.strptime("2015-07-08", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'day-08'), day_nn)
            
        def test_adjust_date_month_nn(self):
            # Verify that adjust_date() returns the correct value 
            # for 'month-nn'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            month_nn = datetime.datetime.strptime("2015-03-23", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'month-03'), month_nn)
            
        def test_adjust_date_year_nn(self):
            # Verify that adjust_date() returns the correct value 
            # for 'year-nn'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            year_nn = datetime.datetime.strptime("2012-07-23", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, 'year-2012'), year_nn)

        def test_adjust_date_days_ago(self):
            # Verify that adjust_date() returns the correct value for
            # 'nn-days-ago'
            today = datetime.datetime.strptime("2015-07-23", "%Y-%m-%d")
            daysago = datetime.datetime.strptime("2015-07-20", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, '3-days-ago'), daysago)
                
        def test_adjust_date_days_ago_across_month(self):
            # Verify that adjust_date() returns the correct value for
            # 'nn-days-ago' when it crosses a month boundary
            today = datetime.datetime.strptime("2015-07-03", "%Y-%m-%d")
            daysago = datetime.datetime.strptime("2015-06-28", "%Y-%m-%d")
            self.assertEqual(self.api.adjust_date(today, '5-days-ago'), daysago)
                
        def test_date_stamp(self):
            # Verify that date_stamp() returns the correct value in the
            # simplest case.
            self.assertEqual(self.api.date_stamp('2015-03-21'), '2015-03-21')
            
        def test_date_stamp_today(self):
            # Verify that date_stamp() returns the correct value for today's
            # date.
            self.assertEqual(self.api.date_stamp('today'), datetime.datetime.now().strftime('%Y-%m-%d'))
            
        def test_invalid_date_stamp(self):
            # Verify that date_stamp() reacts appropriately to an invalid
            # date-string (it should return today's date).
            self.assertEqual(self.api.date_stamp('wrong'), datetime.datetime.now().strftime('%Y-%m-%d'))

        def test_portable_path(self):
            # Verify that portable_path() returns the actual path to the
            # Python script.
            script_path = os.getcwd()
            self.assertEqual(self.api.portable_path(), script_path)
            
        def test_prepare_file(self):
            # Verify that prepare_file() results in an empty contents list.
            self.api.prepare_file()
            self.assertEqual(self.api.contents, [])
            
        def test_save_file(self):
            # Verify that save_file() creates a file
            self.api.add_line("2015-12-10", "This is a test")
            self.api.save_file()
            
    unittest.main()

