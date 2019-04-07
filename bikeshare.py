import time
import pandas as pd
import numpy as np

"""
This project is my first python project that strenghtens the basis in my future career.
I believe that I can do it
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


CITIES = ['chicago', 'new york', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! This is Jay.\nLet\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city do you want to analyze? \nChicago, New york or Washington. \n').lower()
        if city in CITIES:
            break
        else:
            print('You entered invalid city name! Please enter Chicago, New York or Washington. \n')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Input a month you want to analyze or you can just enter \'all\' to apply no month filter \n"
                      "For example- January, February, March, April, May, June or ALL \n").lower()
        if month in MONTHS:
            break
        else:
            print('You entered Invalid month! Please enter a month!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Finally, enter a day of week you want to analyze!\n'
                    'For example- Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or ALL to apply no day filter\n').lower()
        if day in DAYS:
            break
        else:
            print('You entered Invalid day of week! Please enter a day!\n')

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = MONTHS
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most popular times of travel."""

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create new columns for month, weekday, hour
    month = df['Start Time'].dt.month
    weekday_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour

    # display the most common month
    print('The most popular month is: ', month.mode()[0])

    # display the most common day of week
    print('The most popular day of week: ',  weekday_name.mode()[0])

    # display the most common start hour
    print('The most popular start hour: ', hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('Most commonly used end station:', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    trip_stations = df['Start Station'] + "," + df['End Station']
    most_popular_trip = trip_stations.value_counts().idxmax()
    print('The most popular trip is: \n {} ----> {}'.format(most_popular_trip.split(',')[0], most_popular_trip.split(',')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n...Calculating User Stats...\n')
    start_time = time.time()
    # Convert seconds to year, days, hours, minuets, seconds!
    def secs_to_ydhms(seconds):
        m, s = divmod(seconds, 60)  # 60 sec = 1 min
        h, m = divmod(m, 60)    # 60min = 1hour
        d, h = divmod(h, 24)    # 24hours = 1 day
        y, d = divmod(d, 365)    # 365days = 1 year
        print('Years: {}, Days: {}, Hours: {}, Minuets: {}, Seconds: {}'.format(y, d, h, m, s))

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:')
    secs_to_ydhms(total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe average travel time is: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)

    # Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
        print(count_gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        most_recent_birth = df['Birth Year'].max()
        earliest_birth = df['Birth Year'].min()
        common_birth = df['Birth Year'].mode()[0]
        print("\nThe earliest year of birth: " + str(earliest_birth))
        print("The most recent year of birth: " + str(most_recent_birth))
        print("The most common year of birth: " + str(common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    line = 0
    user_input = input('Do you want to see some raw data? Enter either YES or NO.\n')
    while True:
        if user_input.lower() == 'yes':
            print(df.iloc[line: line + 5])
            line += 5
            user_input = input('\nAre you sure you want to see more raw data? Enter YES or NO.\n')
        elif user_input.lower() == 'no':
            break
        else:  #if user input is neither yes nor no!
            user_input = input('\nYou didn\'t enter a proper input.\nDo see more raw data? Enter YES or NO.\n')

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
