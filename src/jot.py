#!/usr/bin/python
# -*- coding: utf-8 -*-
"""jot
A command-line journal for simple daily records.

Usage:
    jot add [for] <date> "<entry>" 
    jot add <entry>
    jot [-x] list all
    jot [-x] list [for] <date>
    jot [-x] list from <fromdate> [to <todate>] [inc|inclusive]
    jot -h | --help
    jot --version

Options:
    -x --expand   Add blank lines between entries
    -h --help     Show this screen.
    --version     Show version.
  
Note that <entry> must be enclosed in double-quotes. 

If no date is specified, today is assumed.

Multiple entries for the same day will be grouped together in order of
entry.

The <date> value can either be a date string in the format yyyy-mm-dd, or
can be one of the following special values:

    - today       - Today's date
    - yesterday   - Yesterday's date
    - this-week   - The first day of the week (Monday)
    - this-month  - The first day of the month
    - this-year   - The first day of the year
    - last-week   - Exactly seven days previous to today
    - last-month  - This day last month (adjusting final days if necessary)
    - last-year   - This day exactly one year ago
    - day-nn      - The specified day of this month
    - month-nn    - The first day of the specified month this year
    - year-nnnn   - The first day of the specified year
    - nn-days-ago - The specified number of days ago
    
"""

# Standard library imports
import datetime
import calendar
import os
import textwrap

# Third party imports
from docopt import docopt

# Application specific imports

class Jot():

    """
    Main processor class, with Processor.execute() as the entry-point.
    """
    def __init__(self):
        self.contents = []
        self.filename = os.path.join(self.portable_path(), "jot.txt")
        
    def execute(self, params):
        self.params = params
        self.load_file()
        self.parse_parameters()
        if self.do_add:
            self.add_line(self.for_date, self.entry)
        elif self.do_list:
            self.list_out()
        self.save_file()
        return True

    def parse_parameters(self):
        """
        Extracts the details from the parameters passed to execute(),
        defaulting any which are not set (in theory docopt should catch
        these, but if execute() is called directly from another script it
        might not be passed all the required entries).
        """
        if "add" in self.params:
            self.do_add = self.params["add"]
        else:
            self.do_add = False
            
        if "list" in self.params:
            self.do_list = self.params["list"]
        else:
            self.do_list = False

        # If neither 'add' nor 'list' was specified, default to 'add'.
        # This allows 'jot "An entry"' as a short-cut for adding an
        # entry to the current day.
        if not self.do_add and not self.do_list:
            self.do_add = True
            
        if "<date>" in self.params:
            self.for_date = self.date_stamp(self.params["<date>"])
        else:
            self.for_date = self.date_stamp("today")
            
        if "<fromdate>" in self.params:
            self.from_date = self.params["<fromdate>"]
        else:
            self.from_date = None
            
        if "<todate>" in self.params:
            self.to_date = self.params["<todate>"]
        else:
            self.to_date = None
            
        if not self.from_date:
            self.from_date = self.for_date
        else:
            self.from_date = self.date_stamp(self.from_date)
        
        if not self.to_date:
            self.to_date = "today"
        else:
            self.to_date = self.date_stamp(self.to_date)
            
        if "all" in self.params and self.params["all"]:
            self.from_date = ""
            self.to_date = "today"
            
        if "<entry>" in self.params:
            self.entry = self.params["<entry>"]
        else:
            self.entry = ""
            
    def subtract_months(self, date, delta):
        m, y = (date.month-delta) % 12, date.year + ((date.month)-delta-1) // 12
        if not m: m = 12
        d = min(date.day, calendar.monthrange(y, m)[1])
        return date.replace(day=d, month=m, year=y)
        
    def adjust_date(self, base_date, adjustment):
        """
        Returns a date that is offset from the supplied base_date by the
        value identified by the adjustment string:
    
            * today       - Today's date
            * yesterday   - Yesterday's date
            * this-week   - The first day of the week (Monday)
            * this-month  - The first day of the month
            * this-year   - The first day of the year
            * last-week   - Exactly seven days previous to today
            * last-month  - This day last month (adjust final days if necessary)
            * last-year   - This day exactly one year ago
            * day-nn      - The specified day of this month
            * month-nn    - The first day of the specified month this year
            * year-nnnn   - The first day of the specified year
            * nn-days-ago - The specified number of days ago
        
        If date_string does not match any of the above, the date is returned
        unchanged.
        """
        # Force to lower-case for comparison purposes
        compare = adjustment.lower()
        
        this_day = base_date.day
        this_month = base_date.month
        this_year = base_date.year
        
        if compare == "today":
            result = base_date
        elif compare == "yesterday":
            delta = datetime.timedelta(1)
            result = base_date - delta
        elif compare == "this-week":
            delta = datetime.timedelta(days = base_date.weekday())
            result = base_date - delta
        elif compare == "this-month":
            result = datetime.datetime(this_year, this_month, 1)
        elif compare == "this-year":
            result = datetime.datetime(this_year, 1, 1)
        elif compare == "last-week":
            delta = datetime.timedelta(7)
            result = base_date - delta
        elif compare == "last-month":
            result = self.subtract_months(base_date, 1)
        elif compare[0:4] == "day-":
            day = int(compare[4:])
            result = datetime.datetime(base_date.year, base_date.month, day)
        elif compare[0:6] == "month-":
            month = int(compare[6:])
            result = datetime.datetime(base_date.year, month, base_date.day)
        elif compare[0:5] == "year-":
            year = int(compare[5:])
            result = datetime.datetime(year, base_date.month, base_date.day)
        elif compare[-8:] == "days-ago":
            days = int(compare.split('-')[0])
            delta = datetime.timedelta(days)
            result = base_date - delta
        else:
            result = base_date
            
        return result
        
    def date_stamp(self, date_string):
        """
        Returns, in yyyy-mm-dd format, the date identified by the passed in
        string. See adjust_date() above for the meaning of date_string.
        """
        try:
            if date_string:
                base_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            else:
                base_date = datetime.datetime.now()
                date_string = "today" 
            result = self.adjust_date(base_date, date_string).strftime('%Y-%m-%d')
        except (TypeError, ValueError):
            base_date = datetime.datetime.now()
            result = self.adjust_date(base_date, date_string).strftime('%Y-%m-%d')
            
        return result

    def add_line(self, date_stamp, entry):
        """
        Compiles the supplied details into a line, storing it in the current
        contents, and returning it.
        """
        self.line = "%s : %s" % (date_stamp, entry)
        position = self.find_insert_position(self.line)
        if position == -1:
            self.contents.append(self.line.strip())
        else:
            self.contents.insert(position, self.line.strip())
        return self.line

    def find_insert_position(self, for_line):
        """
        Searches the current journal contents until it finds an entry which
        is greater than the date stored in the for_line parameter, and
        returns the index position. If no entry can be found, returns -1
        """
        position = 0
        match_with = for_line[:10]
        for line in self.contents:
            if line[:10] > match_with:
                return position
            position += 1
        return -1
        
    def portable_path(self):
        """
        Returns the actual path to this script, so that we save/load details
        in this directory, enabling the script to be run portably.
        """
        return os.path.split(os.path.realpath(__file__))[0]
    
    def load_file(self):
        """
        Loads the Journal file and returns True if it exists, otherwise
        returns False.
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    if line.strip() != "":
                        self.contents.append(line.strip())
            return True
        else:
            return False

    def save_file(self):
        """
        Saves the current Journal to file.
        """
        with open(self.filename, "w") as f:
            f.write("\n".join(self.contents))
        
    def prepare_file(self):
        """
        Prepares the journal file for use, loading one if it exists, 
        otherwise creating a new, empty journal.
        """
        if not self.load_file():
            self.contents = []

    def _date_in_range(self, line_date):
        """
        Only used by list_out. Returns True if the supplied date falls
        within the range specified by the command-line parameters.
        """
        if line_date < self.from_date:
            return False
            
        if self.params["inc"] or self.params["inclusive"]:
            return (line_date <= self.to_date)

        return (line_date < self.to_date)
        
    def list_out(self):
        """
        Prints the journal to STDOUT
        """
        wrapper = textwrap.TextWrapper()
        last_date = ""
        for line in self.contents:
            line_date = line[:10]
            if self._date_in_range(line_date):
                if line_date != last_date:
                    print "# %s" % line_date
                    last_date = line_date
                line = line[13:]
                print wrapper.fill(line)
                if self.params["--expand"]:
                    print

if (__name__ == "__main__"):
    params = docopt(__doc__, version='jrnl, v0.0.0.1')
    # print params

    api = Jot()
    api.execute(params)

