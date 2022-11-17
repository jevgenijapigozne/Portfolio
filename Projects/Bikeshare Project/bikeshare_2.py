import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
cities = ('chicago','new york','washington')  
months = ('january','february','march','april','may','june', 'all')
days = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all')


def check_if_in_the_list(findable, list_to_look_in):
    """
    Check if user specified value is in the list of allowed values
    Args: 
        (str) - value to analise
        (list) - list to check in
    Returns:
        True of False    
    """
    if findable.lower().strip() in list_to_look_in:
        return True
    else:
        print('Please input the correct value, any from the following list: {}.'. format(str(list_to_look_in).title()))
        return False
        
def check_if_col_in_df(col_name,df):
    """
    Check if column exist in the dataframe
    Args: 
        (str) - name of column
        (class pandas.DataFrame) - dataframe to look in
    Return:
        True of False 
    """
    if col_name in df:
        return True
    else:
        return False        

def stay_or_go(choice):
    """
    Check if user wants to exit the program
    Args: 
        (str) -user choice  (yes or no)
        (class pandas.DataFrame) - dataframe to look in
    Return:
        True of False 
    """

    choice = choice.lower().strip()
    while True:
        if choice =='y':
            print('\nWe are sorry that you are leaving us')
            return False
        elif choice =='n':
            return True
        else :
            print ('\nPlease choose Y or N only')
            choice =  str(input('Do you want to exit? Y/N: '))
            choice = choice.lower().strip()
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
      
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    user_choice = 'n'
    while stay_or_go(user_choice):
        city=''
        while city =='' or check_if_in_the_list(city,cities)==False:
            try:
                city = str(input('\nWould you like to see data for Chicago, New York, or Washington? '))
                city = city.lower().strip()
            except KeyboardInterrupt:
                user_choice = str(input('\nDo you want to exit? Y/N: '))
                user_choice = user_choice.lower().strip()
                if stay_or_go(user_choice)== False:
                    exit()
        # get user input for month (all, january, february, ... , june)
        month=''
        while month =='' or check_if_in_the_list(month,months)==False:
            try:        
                month =str(input('Enter the name of the month or all for filtering: '))
                month = month.lower().strip()
            except KeyboardInterrupt:
                user_choice = str(input('\nDo you want to exit? Y/N: '))
                user_choice = user_choice.lower().strip()
                if stay_or_go(user_choice)== False:
                    exit()
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day=''
        while day =='' or check_if_in_the_list(day,days)==False:
            try:
                day = str(input('Enter the day of the week or all for filtering: '))
                day = day.lower().strip()
            except KeyboardInterrupt:
                user_choice = str(input('\nDo you want to exit? Y/N: '))
                user_choice = user_choice.lower().strip()
                if stay_or_go(user_choice)== False:
                    exit()
        break
            
    print('-'*40)
    #print(city, month, day)
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
   
    
    
    file_name = CITY_DATA[city.lower().strip()]
    df = pd.read_csv(file_name)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        # filter by day of week if applicable
        
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day.title()]
        
    df = df.mask(df == '')
    return df
    
##def if_return_more_row(column_name,df):
 
   ## value_and_count = dict()
   ## for value in df[column_name].mode():
      ##  value_and_count[value] = df[column_name].value_counts()[value]
    ##return value_and_count

def time_stats(df, user_month, user_day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    if user_month.lower() == 'all':
        for month_id in df['Month'].mode():
            month = months[month_id-1]
            month_count = df['Month'].value_counts()[month_id]
            print('\nthe most common month of travel: {} \nrecords for users travelled in {}: {}'.format(month.title(),  month.title(), month_count))
    # display the most common day of week
    if user_day.lower() == 'all':
        for day in df['Day of week'].mode():
            day_count = df['Day of week'].value_counts()[day]
            print ('\nthe most popular day of week: {} \nrecords for users travelled on {}: {}'.format(day,day,day_count)) 
       
    # display the most common start hour 
    df['Hour'] = df['Start Time'].dt.hour
    for hour in df['Hour'].mode():
        hour_count = df['Hour'].value_counts()[hour]
        print('\nthe most common start hour: {} o\'clock \nrecords for users travelled at {} o\'clock: {}'.format(hour, hour, hour_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    for start_station in df['Start Station'].mode():
        start_station_count = df['Start Station'].value_counts()[start_station]
        print('\nthe most commonly used start station: {}. \nrecords of users departed from {}: {}'.format(start_station, start_station, start_station_count))
    
    # display most commonly used end station
    for end_station in df['End Station'].mode():
        end_station_count = df['End Station'].value_counts()[end_station]
        print('\nthe most commonly used end station: {}. \nrecords of users arrived to {}: {}'.format(end_station, end_station, end_station_count))

    # display most frequent combination of start station and end station trip

    for popular_combination in('from ' + df['Start Station'] + ' to ' + df['End Station']).mode():
        popular_combination_count = ('from ' + df['Start Station'] + ' to ' + df['End Station']).value_counts()[popular_combination]
        print('\nthe most frequent station combination: {}. \nrecords of users travelled {}: {}'.format(popular_combination, popular_combination, popular_combination_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_s = df['Trip Duration'].sum()
    total_travel_time_min = total_travel_time_s//60
    total_travel_time_min_s = total_travel_time_s%60
    total_travel_time_hour = total_travel_time_s/60//60
    total_travel_time_hour_min =  total_travel_time_s/60%60
    total_travel_time_day = total_travel_time_s/60/60//24
    total_travel_time_day_hour = total_travel_time_s/60/60%24
    print('\nTotal travel time was : \n\n{} seconds or \n{} minutes and {} seconds or \n{} hours, {} minutes and {} seconds or \n{} days, {} hours, {} minutes, {} seconds.'.format(int(total_travel_time_s), int(total_travel_time_min), int(total_travel_time_min_s), int(total_travel_time_hour), int(total_travel_time_hour_min), int(total_travel_time_min_s), int(total_travel_time_day), int(total_travel_time_day_hour), int(total_travel_time_hour_min), int(total_travel_time_min_s)))
    
    # display mean travel time
    average_travel_time_s = int(df['Trip Duration'].mean())
    average_travel_time_min = average_travel_time_s//60
    average_travel_time_min_s = average_travel_time_s%60
    print('\nAverage travel time was : \n\n{} seconds or \n{} minutes and {} seconds.'.format(average_travel_time_s, average_travel_time_min, average_travel_time_min_s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_count = df['User Type'].count()
    subscriber_count = df['User Type'].value_counts()['Subscriber']
    customer_count = df['User Type'].value_counts()['Customer']
    if  any (df['User Type']=='Dependent'):
        dependent_count = df['User Type'].value_counts()['Dependent']
    else :
        dependent_count = 0    
    unknown_type_count = df['User Type'].isna().sum()
    print('\nRecords of service users travelled for this period : {}\n\nsubscribers: {} \ncustomers: {} \ndependants: {} \nunknown status: {}'.format(user_count+unknown_type_count, subscriber_count, customer_count, dependent_count, unknown_type_count))

    # Display counts of gender
    if check_if_col_in_df('Gender', df):
        male_count = df['Gender'].value_counts()['Male']
        female_count = df['Gender'].value_counts()['Female']
        unknown_gender_count = df['Gender'].isna().sum()
        print('\nfemale users: {} \nmale users: {} \ngender unknown: {}'.format(female_count, male_count, unknown_gender_count))
    
    # Display earliest, most recent, and most common year of birth
    if check_if_col_in_df('Birth Year', df):
        oldest = int(df['Birth Year'].min())
        oldest_count = df['Birth Year'].value_counts()[oldest]
        youngest = int(df['Birth Year'].max())
        youngest_count = df['Birth Year'].value_counts()[youngest]
        for common in df['Birth Year'].mode():
            common_count = df['Birth Year'].value_counts()[common]
            print('\n{} records for users born in earliest year: {} \n{} records for users born in latest year: {} \n{} records for users sharing the most common birth year: {}'.format( oldest_count, oldest, youngest_count, youngest, common_count, int(common)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    user_choice = 'n'
    while stay_or_go(user_choice):
        user_city, user_month, user_day = get_filters()
        user_database = load_data(user_city, user_month, user_day)
        time_stats(user_database, user_month, user_day)
        station_stats(user_database)
        trip_duration_stats(user_database)
        user_stats(user_database)
        user_choice = str(input('\nDo you want to exit? Y/N : ')).lower().strip()


if __name__ == "__main__":
    


    main()
