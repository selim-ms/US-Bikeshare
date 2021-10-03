#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
import pandas as pd
import numpy as np
import datetime
import calendar
pd.set_option('display.max_columns',200)


# In[9]:


def Time_converter(seconds):
    '''Converts time from seconds to Hours, Minutes & Seconds'''
    hrs = seconds//3600 #calculates Hours
    mins = (seconds%3600)//60 #calculates remainder in minutes
    secs = (seconds%3600)%60 #calculates remainder in seconds
    duration = '{} Hours, {} Minutes & {} Seconds'.format(hrs, mins, secs)
    return duration


# In[10]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Available cities are Chicago, New York City & Washington, choose a city by typing its name:").lower()
        if city not in CITY_DATA:
            print('Please select a valid city with the right spelling & syntax')
        else:
            break
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter a month to analyse or enter 'ALL' to select the full period \n knowing that the data set covers the period from January to June ").title()
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        if month not in months and month != 'All':
            print('Please enter a valid month between January & June (inclusive) with the right spelling')
        else:
            break
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Choose a day of the week Monday to Sunday by entering the first three letters of it \n or enter 'All' to select the full period ").lower()
        days = {'mon':'Monday','tue':'Tuesday','wed':'Wednesday','thu':'Thursday','fri':'Friday','sat':'Saturday','sun':'Sunday'}
        if day not in days and day != 'all':
            print('Please enter a valid choice')
        else:
            if day != 'all':
                day = days[day]
            break
    
    print('-'*40)
    return city, month, day


# In[11]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) month - name of the month to filter by, or "all" to apply no month filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city]) #reads file from input city name
    
    df['Start Time']=pd.to_datetime(df['Start Time']) #structures date & time format
    df['month']=df['Start Time'].dt.month_name() #adds month column
    df['week_day']=df['Start Time'].dt.day_name() #adds day column
    df['hour']=df['Start Time'].dt.hour #adds hour column
    df['Trip']=df['Start Station'] + ' -> ' +df['End Station'] #adds Trip column
    
    if month != 'All':
        df=df[df['month'] == month] #adds a filter for months if needed
    
    if day != 'all':
        df=df[df['week_day'] == day.title()] #adds a filter for days if needed
    
    

    return df


# In[12]:



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is :", df['month'].mode()[0])

    # TO DO: display the most common day of week
    print("The most common day is :", df['week_day'].mode()[0])

    # TO DO: display the most common start hour
    print("The most common hour is :", df['hour'].mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time)) #calculates time taken to complete the opertions
    print('-'*40)


# In[13]:



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: ",df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most common destination is: ",df['End Station'].mode()[0])    

    # TO DO: display most frequent combination of start station and end station trip
    print("The most common trip is: ",df['Trip'].mode()[0])    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



# In[14]:



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time=df['Trip Duration'].sum() #calculates the total time in seconds
    print('The total travel time is ', Time_converter(total_time))    
    # TO DO: display mean travel time
    average_time=df['Trip Duration'].mean() #calculates the average time in seconds
    print('The average travel time is ', Time_converter(average_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



# In[15]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Counts are categorized below: \n', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('User Genders are categorized below: \n', df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest birth year is: ',int(df['Birth Year'].min()))
        print('The most recent birth year is: ',int(df['Birth Year'].max()))
        print('The most common birth year is: ',int(df['Birth Year'].mode()[0]))
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[16]:


def raw_data(df):
    ''' Shows a 5 row sample of the filtered data frame if the user wants to check a quick sample '''
    row_count = 0 #setting row number variable to zero
    while True: #while loop to exclude incorrect inputs
        decision = input('Would you like to view a new sample of raw data from row {} to row {}? (Y/N)'.format(row_count+1, row_count+5)).lower()
        if decision == 'y':
            print(df[row_count:row_count+5]) #print the next 5 rows of the dataframe
            row_count += 5 #adds 5 to the row count to avoid showing the same data sample
        elif decision == 'n':
            break
        else:
            print('Please provide a valid input Y or N')


# In[17]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[18]:





# In[ ]:




