import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'ny': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = {'jan': 'January', 'feb': 'February',
          'mar': 'March', 'apr': 'April',
          'may': 'May', 'jun': 'June'}

weekdays = {'mon': 'Monday', 'tues': 'Tuesday',
            'wed': 'Wednesday', 'thur': 'Thursday',
            'fri': 'Friday', 'sat': 'Saturday', 'sun': 'Sunday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "no" to apply no month filter
        (str) day - name of the day of week to filter by, or "no" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # handles invalid inputs by allowing to re-enter input
    while True:
        city = input('Enter city from (chicago, new york city(or ny), washington) for exploration: ').strip().lower()
        if city in CITY_DATA.keys():
            break

    # asks for refine data with filters
    filter_option = input('Do you want filter options? (y/n): ')
    if filter_option in ('yes', 'y'):

        # gets user input for abbreviation(abbr) of month
        filter_month_option = input('Filter by month? (y/n): ').strip()
        if filter_month_option in ('yes', 'y'):
            while True:
                month_abbr = input('Enter month to be filtered with \n' +
                                   f'{months.keys()}: ').strip()
                print(month_abbr)
                if month_abbr in months.keys():
                    month = months[month_abbr]
                    break
        else:
            # no filter applied for month
            month = 'all'

        # gets user input for abbreviated(abbr) day of week
        day_filter_option = input('Filter by Day? (y/n): ').strip()
        if day_filter_option in ('yes', 'y'):
            while True:
                day_abbr = input('Enter any day of week as \n' +
                                 f'{weekdays.keys()}: ').strip()
                print(day_abbr)
                if day_abbr in weekdays:
                    day = weekdays[day_abbr]
                    break
        else:
            # no filter applied for day
            day = 'all'

    else:
        # no filter is applied at all
        month, day = 'all', 'all'

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    path = './data/'
    filename = path + CITY_DATA[city]

    print('Loading Data ....')

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    # df['month'] = df['month'].str.lower()

    df['weekday'] = df['Start Time'].dt.strftime('%A')
    # df['weekday'] = df['weekday'].str.lower()

    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['weekday'] == day]

    print('Data Loaded !', '\n')
    print('-' * 40)
    return df


def nan_stats(df):
    """Displays Statistics of NaN values in DataFrame"""

    print('Status of NaN values ...', '\n')
    print("Rows count with nan\'s: ", df.shape[0])
    print('Total NaN counts: ', df.isnull().any(axis=1).sum())


def remove_nan(df):
    """Removes NaN values INPLACE from dataframe"""

    print('Removing NaN valued rows from data...')
    df.dropna(axis=0, inplace=True)
    print("Row Counts without nan's", df.shape[0])


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Riders mostly seen to ride in months: ',
          df['month'].mode().values)

    # display the most common day of week
    print('Riders rides mostly on weekdays: ',
          df['weekday'].mode().values)

    # display the most common start hour
    print('Common riding hour:',
          df['hour'].mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common Start Station is: \n',
          df['Start Station'].mode().values, '\n')

    # display most commonly used end station
    print('Most common End Station is: \n',
          df['End Station'].mode().values, '\n')

    # display most frequent combination of start station and end station trip
    df_paired_group = df.groupby(['Start Station', 'End Station']).size()
    start, end, count = df_paired_group.sort_values(ascending=False).reset_index().values[0]
    print('Frequent combination of Start Station, End Station and frequency: \n',
          '    Start: ', start, '\n',
          '    End: ', end, '\n'
          '    Frequency: ', count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('Total Travel time of all riders took nearly: {:.1f} hrs'.format(
          tot_travel_time / 60))

    # display mean travel time
    avg_trav_time = df['Trip Duration'].mean()

    print('The Average Ride time for each person is: {:.1f} hrs'.format(avg_trav_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The No. of Users & User types riding are: ')
    print(df['User Type'].value_counts(), '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Gender Counts are: \n',
              df['Gender'].value_counts())
    else:
        print('No Gender Data available')

    print()
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('First ride taken can be seen back to year: ',
              int(df['Birth Year'].min()), '\n')

        print('Most updated ride taken on year: ',
              int(df['Birth Year'].max()), '\n')

        print('Riders riding with common birth years: ',
              tuple(map(int, df['Birth Year'].mode())),
              '\n')

    else:
        print('No birth year data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    """ Asks user interactively to show portion of raw data """

    show_data_option = input('Care to see some raw data from city data? (y/n): ').strip().lower()
    if show_data_option in ('yes', 'y'):
        print('Data Limit: ', df.shape[0])
        for i in range(5, df.shape[0], 5):
            print(df.iloc[i - 5:i])
            more_data = input('Want to see more data (y/n): ').strip().lower()
            if more_data in ('no', 'n'):
                break


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        # raw data display
        show_data(df)  # done

        # counting NaN values
        nan_stats(df)

        # dealing with NaN values
        remove_nan(df)

        print('-' * 40)

        time_stats(df)  # done
        station_stats(df)  # done
        trip_duration_stats(df)  # done
        user_stats(df)  # done

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
    main()
