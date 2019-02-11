import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ("all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
DAYS = ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():
        city = input('Please, enter the city "Chicago", "New York City", "Washington" \n').strip().lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTHS:
        month = input('Please, choose the month from the set\n("all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december") \n').strip().lower()
    month = month.capitalize()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in DAYS:
        day = input('Please, choose the day of the week from the set \n("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")\n').strip().lower()
    day = day.capitalize()

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
    # https://stackoverflow.com/questions/45489846/filter-out-rows-from-a-column-in-python-pandas
        # add two columns of month and day to filter
  #  df['Start Time'] = pd.to_datetime(df['Start Time'])


    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Time (hour)'] = df['Start Time'].dt.hour
    df['month_ind'] = df['Start Time'].dt.month
    df['month'] = df['month_ind'].apply(lambda x: calendar.month_name[x])
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month == 'All' and day != 'All':
        df = df[(df.day_of_week == day)]
    elif month != 'All' and day == 'All':
        df = df[(df.month == month)]
    elif month != 'All' and day != 'All':
        df = df[(df.month == month) & (df.day_of_week == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df.month.mode()[0]
    print('The most common month/s is', common_month)

    # display the most common day of week
    common_day = df.day_of_week.mode()[0]
    print('The most common day of the week is', common_day)

    # display the most common start hour
    common_start_hour = df['Start Time (hour)'].mode()[0] # need to check column names
    print('The most common start hour is', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is', end_station)

    # display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start and end station trip is', start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    print('Counts of user types \n', counts_user_types)


    # Display counts of gender
    if 'Gender' not in df.keys():
        print('\nNo "Gender" data in this file')
    else:
        counts_of_gender = df['Gender'].value_counts()
        print('\nCounts of gender \n', counts_of_gender)


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.keys():
        print('\nNo "Birth Year" data in this file')
    else:
        min_date = df['Birth Year'].min()
        max_date = df['Birth Year'].max()
        common_date = df['Birth Year'].mode()[0]
        print('\nThe earliest year of birth is', int(min_date))
        print('The most recent year of birth is', int(max_date))
        print('The most common year of birth is', int(common_date))


    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            #try:
            user_stats(df)
            #except Exception:
            print('\nThere are no user stats in this file')
        else:
            print('\nThere are no data for this period, try another month/day')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
#some comments added


if __name__ == "__main__":
	main()
