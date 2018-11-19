#!/usr/bin/env python3

#request and json needed for API call to worldtimeapi.org.
import requests
import json
#time needed convert from ISO 8601 format of time to structed.
import time
#decimal needed to convert from integer to rounded float with two decimal places.
from decimal import Decimal
#pprint used to print JSON in a pretty format for testing.
from pprint import pprint
#used to print exception info/testing.
import sys

#function to get time information via worldtimeapi.org via API call.
def world_time_API():
    #get information from user (timezone) to construct the URL for the "GET" API call.
    vf_str_baseURL = 'http://worldtimeapi.org/api/timezone'
    print('There is a large list of timezones/locations to choose from.  Please visit http://worldtimeapi.org/timezones for more information.')
    vf_str_timezone = input('timezone: ')
    #while loop for error checking to make sure value isn't blank.
    while vf_str_timezone == '':
       vf_str_timezone = input('enter a real timezone: ')
    vf_str_fullURL = vf_str_baseURL + '/' + vf_str_timezone
    #try the api call, if there is any exception print an eror and stop the program.  This will mostly likely be caused by connection issue to worldtimeapi.org or DNS issues.
    try:
        vf_req_response = requests.request('GET', vf_str_fullURL)
    except:
        print('could not connect to worldtimeapi.org, please check your internet connection/DNS and try again')
        ###print(sys.exc_info())
        exit()
    #if there was a response code (connection to website) but it didn't return a 200 response, most likely a bad timezone was entered.  Print error and stop program.
    if vf_req_response.status_code != 200:
        print('bad entry, please run script again')
        exit()
    #if there is a 200 code store respone as variable, parse the 'datetime' key, and remove the last 13 character to make it into ISO 8601 format.  Then return to main.
    vf_dic_parse = json.loads(vf_req_response.text)
    vf_str_datetime = vf_dic_parse['datetime']
    vf_str_datetime = vf_str_datetime[:-13]
    return vf_str_datetime

#function to take ISO formated date from world_time_API function and extract parts for printing.  Values passed back as dictionary for simplicity.
def ISO_to_var(vf_str_datetime):
    #first parse the ISO format string value into a tuple of year, month, day, hour, minute, second values
    vf_tup_time = time.strptime(vf_str_datetime, '%Y-%m-%dT%H:%M:%S')
    #next, parse the individual values from the tuple to be consolodated into a dictionary
    vf_str_weekday = time.strftime('%A',vf_tup_time)
    vf_str_month = time.strftime('%B',vf_tup_time)
    vf_int_daynum = int(time.strftime('%d',vf_tup_time))
    vf_str_year = time.strftime('%Y',vf_tup_time)
    #number of days in month is necessary to calculate days left in the current month.  However, this can change depending on it being a leap year or not.
	#send value of 'year' to check_leap_year to determine if it is a leap year or not, and then get the appropriate month/days in month mapping (dictionary).
    vf_dict_monthday = check_leap_year(vf_str_year)
    #integer days in month is found via the dictionary.  Days left is month is day in month minus current day value.
    vf_int_days_in_month = vf_dict_monthday[vf_str_month]
    vf_int_days_left = vf_int_days_in_month - vf_int_daynum
    #calcuate standard vs military times from tuple
    vf_str_stan_time = time.strftime('%I:%M%p',vf_tup_time)
    vf_str_mil_time = time.strftime('%H%M',vf_tup_time)
    #find total hours, minutes and seconds to calculate total seconds since midnight.
    vf_int_minutes = int(time.strftime('%M',vf_tup_time))
    vf_int_hours = int(time.strftime('%H',vf_tup_time))
    vf_int_sec = int(time.strftime('%S',vf_tup_time))
    vf_int_sec_since_midnight = (((60 * vf_int_hours) + vf_int_minutes) * 60) + vf_int_sec
    #decimal is an easy way to make an integer a float and then round up after two decimal places.
	#percent of day left is calculated from (seconds left in day)/(total seconds in day) times 100.
    vf_dec_percent_left = Decimal(100 * ((86400 - vf_int_sec_since_midnight)/86400))
    vf_dec_percent_format = round(vf_dec_percent_left,2)
    #best to passback to main a dictionary rather than a bunch of individual variables
    vf_dict_return_values = {'weekday':vf_str_weekday,'month':vf_str_month,'day':vf_int_daynum,'year':vf_str_year,'daysleft':vf_int_days_left,'standard':vf_str_stan_time,'military':vf_str_mil_time,'midnight':vf_int_sec_since_midnight,'daypercent':vf_dec_percent_format}
    return(vf_dict_return_values)

#function to check if current year is a leap year and pass back dictionary of month/days in month mapping.
def check_leap_year(vf_str_year):
    #set dictionaries for a regualr year and leap year (only difference in February).
    vf_dict_monthday_reg = {'January':31,'February':28,'March':31,'April':30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30,'December':31}
    vf_dict_monthday_leap = {'January':31,'February':29,'March':31,'April':30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30,'December':31}
    #to determine if a year is a leap year, we need to check if it is divisible by 4, 100 and 400
    #explained here: https://science.howstuffworks.com/science-vs-myth/everyday-myths/question50.htm
    #convert year to integer and test if divisible by 4 first.
    vf_int_year = int(vf_str_year)
    if vf_int_year % 4:
        #not divisible by 4 - not a leap year - return regular dictionary
        return(vf_dict_monthday_reg)
    elif vf_int_year % 100:
        #divisible by 4 but not 100 - leap year - return leap dictionary
        return(vf_dict_monthday_leap)
    elif vf_int_year % 400:
        #divisible by 4 and 100 but not 400 - not a leap year - return regular dictionary
        return(vf_dict_monthday_reg)
    else:
        #divisible by 4, 100 and 400 - leap year - return leap dictionary
        return(vf_dict_monthday_leap)
        
#function to print time values for user        
def print_info(vf_print_val):
    ##sep='' is needed to get rid of extra spaces
    print(vf_print_val['weekday'],', ',vf_print_val['month'],' ',vf_print_val['day'],', ',vf_print_val['year'],'.',' There are ',vf_print_val['daysleft'],' days left in the month.',sep='')
    print(vf_print_val['standard'],' or ',vf_print_val['military'],' hours',sep='')
    print(vf_print_val['midnight'],' seconds since midnight',sep='')
    print(vf_print_val['daypercent'],'% of the day remains',sep='')
  
#main program: best practice to separate parts of program into function and call from main for reusable code and having the ability to add/remove features.  
if __name__ == '__main__':
    #call world_time_API and store value as string.
    vm_str_datetime = world_time_API()
    #pass the return value of world_time_API into ISO_to_var and store as dictionary.
    vm_dict_returnvalues = ISO_to_var(vm_str_datetime)
    #pass return value of ISO_to_var into print_info, program complete! And Bob's your uncle!
    print_info(vm_dict_returnvalues)