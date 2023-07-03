import time
import pandas as pd
import numpy as np
import datetime as datetime
import pdb
pd.set_option('display.max_columns', None)

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data today !')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Which city would you like to view data for: Chicago, New York City, "
                         "or Washington? ").lower()
            if city in ['chicago', 'new york city', 'washington']:
                break
            else:
                print("That's not a valid selection. Please re-enter.")
        except:
            print("That's not a valid selection. Please re-enter")
    #get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Which month would you like to view data for: January, February, March, April, May, "
                          "June, or All ? ").lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("That's not a valid entry. Please try again.")
        except:
            print("That's not a valid entry. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input(
            "Which day would you like to view data for: Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,"
            "Sunday, or All  ? ").lower()
            if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("That's not a valid entry. Please try again.")
        except:
            print("That's not a valid entry. Please try again.")

        print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', common_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " ----- to ----- " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print('Most Common Trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()/60/60
    print(f"The total travel time is {total_travel_time.round(2)} hours.")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print(f"The mean travel time is {mean_travel_time.round(2)} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser types...')
    user_types = df['User Type'].value_counts()
    for i, user_type in enumerate(user_types.index):
        print(f"{user_type}: {user_types.values[i]}")

    # Display counts of gender
    print('\nGender count and birth year data ...')
    try:
        gender_count = df['Gender'].value_counts()
        for i, gender in enumerate(gender_count.index):
            print(f"{gender}: {gender_count.values[i]}")

        # Display earliest, most recent, and most common year of birth
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe oldest user is born in {}, the youngest user is born in {}, the most common birth year {}."
              .format(oldest, youngest, common_year))
    except:
        print('\nNo data available')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data for users"""

    print('\nDisplay Raw Data .......\n')

    start_loc = 0
    end_loc = 5
    df = df.iloc[-7:]
    max_rows = df.shape[0]

    while True:
        user_input = input("Do you want to view raw data ? (y/n) :").lower()
        if user_input == "y":
            if end_loc <= max_rows:
                print(df.iloc[start_loc:end_loc])
                start_loc += 5
                end_loc += 5
            else:
                print(df.iloc[start_loc:end_loc])
                print("\nNo further data available\n ")
                break
        elif user_input == "n":
            break
        else:
            print("\nInvalid selection, please enter 'y' or 'n'\n ")
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


