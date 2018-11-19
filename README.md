# __Johnny's Super Cool Python Time Program Extravaganza!__

> This document uses Markdown.  Please view on Github (https://github.com/johnnywilkes/NPL_NOV_2018_TIME) or use the following for viewing: https://stackedit.io/app#

## ___Overal Program Idea___

In what might be considered a bold and unique move, I decided to take on all the bonus questions in one fell swoop.  I was considering doing this with NTP with something like:

    >>> import ntplib
    >>> from time import ctime
    >>> c = ntplib.NTPClient()
    >>> response = c.request('pool.ntp.org')
    >>> response
    <ntplib.NTPStats object at 0x6ffffd48978>
    >>> response.tx_time
    1541534145.930704
    >>> from datetime import datetime
    >>> local = datetime.fromtimestamp(response.tx_time)
    >>> local
    datetime.datetime(2018, 11, 6, 14, 55, 45, 930704)  
    >>> import pytz    
    >>> tz1 = pytz.timezone('CST6CDT')
    >>> tz1
    <DstTzInfo 'CST6CDT' CST-1 day, 18:00:00 STD>
    >>> local.astimezone(tz1)
    datetime.datetime(2018, 11, 6, 13, 55, 45, 930704, tzinfo=<DstTzInfo 'CST6CDT' CST-1 day, 18:00:00 STD>)

However, I found a handy website called http://worldtimeapi.org which allows API calls to get the local time for any timezone in the entire world!  This seemed like a good alternative, even though they do mention that their website shouldn't be used as a NTP substitute (but for the purposes of this exercise it should suffice).  One advantage is that `ntplib` is a library that had to be installed on your box, while the modules for API calls (requests and json) are standard (no additional install).

I will talk about ways I could have done things differently in the last section (Possible Refactoring/Feature Releases) as it could have been possible to allow both methods (worldtimeapi.org and NTP).  Other methods such as Google Geo Time and the option to allow users to select local time or local time of an IP were considered as well.  However, I find in automation, it is always best to work on the "which and dirty" solution, documenting along the way, and always thinking of incremental improvements.  As long as you structure your program in a way that facilitates improvements (a set of small functions and comments for documentation), this should be easy.

So in summary, I wanted to accomplish all the bonus items, document well, set the bar time, have fun, but not go overboard!  Let me know if you think I achieved all these goals!


## ___Variable Naming/Program Structure___

It was interesting to read over the PEP 8 style guide for python, as I was able to learn a few things.  This was also my first shot at using Python3 rather than 2.7, so it was an overall rewarding learning process.  I was used to having variables as either all uppercase or camelcase, so this was a bit of the change (same goes for function names).  My format for variables was the following:
 - First letter or variable is always "v" to signify that it is a variable.
 - Next letter is either "f" for function or "m" for main.  This signified if the variable was either inside a function (locally significant) or part of the main program.
 - After a underscore, I would note three letters for what type of variable is was.  Examples are str for string, dec for decimal, int for integer, tup for tuple, and dic for dictionary.
 - After another underscore I would have information to describe variable, possibly separated by one or more other underscore to make it easily readable.
 - The only parts that were capitalized were acronyms such as API, URL, ISO, etc.

It is best practice to segregate a program into smaller chucks call functions and this is something I did in this small program.  Functions can make the code easier to read, allow you to re-use code down the line, and make it easier to add features in the future.  My understanding is that it is best to have the function called from the main program instead of having a chain of functions calling each other.  However, there are times that it might be necessary for one function to call another (such as `check_leap_year` in my code) especially if there is a one-to-one dependency of said functions.  Putting the logic of selecting function to call in the main gives the most flexibility of adding/removing functions (for different requirements/features) in the future as well.

It is always good to add sufficient comments within the program, but there is also a fine line in overdoing it.  Please let me know if you think I did two much of it in my program.  I find that it shouldn't be necessary to descrive each and every line of code, but to explain what each function is there to do as well as some of basics on the variables, flow and loops of the program is important.  I also believe there should be mutliple types of comments:
 - A single "#" is for a general comment for a user to follow when looking at the program.  These are the most common.
 - A double "#" (or `##`) is more of an internal comment to remind myself of certain aspects.  These are less common and could possibly be removed.
 - A triple "#" (or `###`) is for a line that is commented out because it isn't necessary for the program to run.  However, it might be kept as an object that is useful to uncomment if necssary (such as showing more detailed error information).  In the future it might be best to have these all under conditional statements if the program is run under a verbose setting:
    ```
    import sys
    if sys.argv[1] == "verbose"
        print(sys.exc_info())
    ```

    
## ___Why I deserve all the Kudos___

I have accomplished the main task as well as the bonus items.  Additionally, I believe I have gone above and beyond of a few items:

We all know that attention to detail is important for any type of engineering.  Also, making your program as future-proof as posible is very important.  One important detail that others might have overlooked is leap years.  Even though I have not intention to run this program during the next leap year (2020), I know I wouldn't want to write a program that I know would malfunction (give inaccurate data) in the future.  Calculating leap year is actually more complicated than I knew:
https://science.howstuffworks.com/science-vs-myth/everyday-myths/question50.htm
I used to think that it just involved seeing if the year was divisible by four, but it is combination of finding out if it is (or isn't) divisible by four, one hundred and four hundred.

Error checking and input validation are also very important in any program.  I have several examples of this in my program, including a while loop to make sure that the users input for timezone isn't blank.  There are also several failure scenarios because worldtimeapi.org requires connection to the internet and DNS to work.  Additionally, a user can always enter a bad timezone entry, so they should be told when they might have done so.  In both cases I decided to stop the entire program instead of outputing a bunch of errors to the user.

We all know that documentation is key for collaboration (or in this case, judging a coding competition).  Comments within the program can act as documentation, but I think a readme (like this one) can be very useful as well.  I also decided I needed to share the code and readme on GitHub as well.  To me, coding without a Git solution is like turkey without gravy, or pumpkin pie without whipped cream on top!  Hopefully you feel the same way!

In summary, if you don't think I have been super nice with this program (especially the documentation), LEMME KNOW!!!!


## ___Possible Refactoring/Feature Releases___

As I noted before, I always like to focus on a quick and easy (and simple) way to tackle a problem and note potential refactors along the way.  This program was no different.  I started with the main task and then focused on the bonus material.  I also felt it was important to have a well-documented program with less "bells and whistles" rather than a suped up program with crap documentation.  Here are some ways I can improve my program in the future:

Add feature for worldtimeapi.org local time for IP address: worldtimepai.org also has an option to look up the local time of an IP address you enter into the API call.  I have done some testing and it seems pretty reliable.  I would be cool to add a menu in the future to have users either select timezone or IP to find local time.

Add functions for NTP or local time and give user options: As noted before, finding local time through NTP (using `ntplib`, `datetime`, and `pytz`) isn't a difficult task.  The `pytz` library also seems to use most if not all of the timezones names used by worldtimeapi.org.  It would be nice in the future if there would be an option for a user to find local time from either: NTP, worldtimeapi.org, or local (or maybe more than one to see if there are differences).

Add feature for Google Geo Time: Google has NTP servers, but they also have an API call where you submit longitude/latitude coordinates to them and they will give you the local time.  Finding the coordinates can be easy as finding a destination on GoogleMaps and right-clicking for the information.  However, this seemed like it needed more of a tutorial and was more complicated, therefore I decided worldtimeapi.org would be a better starting point.  However, it the future it would be cool to have that futctionality.  For more information:
 - https://developers.google.com/maps/documentation/timezone/intro 
 - https://developers.google.com/maps/documentation/geocoding/intro
 - http://www.mapcoordinates.net/en
 - https://www.wikihow.com/Get-Latitude-and-Longitude-from-Google-Maps

Example extended menu:
```
    Welcome to Johnny's Super Cool Python Time Program Extravaganza!!!
    Please select your option or 'q' to quit!
        1. worldtimeapi timezones
        2. worldtimeapi IP address
        3. NTP
        4. local machine time
        5. GoogleMaps Coordinates
    Please enter selection:
```

