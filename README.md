# Jot
_Command-line Journal for simple daily records._

Usage

    jot add [for] <date> <entry>
    jot add <entry>
    jot [-x] list all
    jot [-x] list [for] <date>
    jot [-x] list from <fromdate> [to <todate>] [inc|inclusive]
    jot -h | --help
    jot --version

Options

    -x --expand   Add blank lines between entries
    -h --help     Show this screen.
    --version     Show version.
  
Note that the entry must be enclosed in double-quotes. 

If no date is specified, today is assumed.

Multiple entries for the same day will be grouped together in order of
entry.

The date value can either be a date string in the format yyyy-mm-dd, or
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

The entries are stored in a jot.txt file which will be created in the same location
as the jot script (this allows the system to be used on a portable drive).

## Examples

### Adding entries

    jot add "If no date is specified, it will be added as an entry for the current date."
    jot add for today "This will also be added as one of today's entries."
    jot add for yesterday "Add an entry for yesterday."
    jot add for 2015-05-01 "Add an entry for the 1st of May, 2015"

The 'for' is entirely optional.

### Listing entries

List all entries

    jot list

List all entries for today

    jot list today

List all entries in November

    jot list from 2015-11-01 to 2015-11-30 inclusive

Lists all entries from last week (because 'inclusive' is not specified, it
lists all entries from the start of last week up to -- but not including --
the start of this week)

    jot list from last-week to this-week
