import pandas as pd
import datetime as dt
import random
import time
import os
import matplotlib.pyplot as plt

columns = ['Name', 'Start Date', 'End Date', 'Implementation time']
start_timestamp = 1546300800  # 01-01-2019
end_timestamp = 1577836799  # 31-12-2019
working_hours_start = 8
working_hours_end = 18
working_day_in_hours = working_hours_end - working_hours_start

# 1, 2, 3, 4, 5, 6 и 8 января - Новый год;
# 7 января - Рождество Христово;
# 23 февраля - День защитника Отечества;
# 8 марта - Международный женский день;
# 1 мая - Праздник Весны и Труда;
# 9 мая - День Победы;
# 12 июня - День России;
# 4 ноября - День народного единства.
holidays = [
    dt.datetime(year=2019, month=1, day=1).date(),
    dt.datetime(year=2019, month=1, day=2).date(),
    dt.datetime(year=2019, month=1, day=3).date(),
    dt.datetime(year=2019, month=1, day=4).date(),
    dt.datetime(year=2019, month=1, day=5).date(),
    dt.datetime(year=2019, month=1, day=6).date(),
    dt.datetime(year=2019, month=1, day=7).date(),
    dt.datetime(year=2019, month=1, day=8).date(),
    dt.datetime(year=2019, month=2, day=23).date(),
    dt.datetime(year=2019, month=3, day=8).date(),
    dt.datetime(year=2019, month=5, day=1).date(),
    dt.datetime(year=2019, month=5, day=9).date(),
    dt.datetime(year=2019, month=6, day=12).date(),
    dt.datetime(year=2019, month=11, day=4).date()
]


def get_random_date_range():
    start_date_timestamp = random.randint(start_timestamp, end_timestamp)
    start_date = dt.datetime.fromtimestamp(start_date_timestamp).replace(minute=0, second=0)

    end_date_timestamp = random.randint(start_date_timestamp, end_timestamp)
    end_date = dt.datetime.fromtimestamp(end_date_timestamp).replace(minute=0 if random.randint(0, 1) else 30, second=0)

    # random timedelta under 1 week
    # days = random.randint(0, 7)
    # hours = random.randint(0, 23)
    # minutes = 0 if random.randint(0, 1) else 30
    #
    # end_date = start_date + dt.timedelta(days=days,
    #                                      hours=hours,
    #                                      minutes=minutes)

    return start_date, end_date


def get_implementation_time(row):
    start_date = row['Start Date']
    end_date = row['End Date']

    if start_date.date() == end_date.date():
        if start_date.weekday() not in [5, 6] and start_date.date() not in holidays:
            implementation_time = max(min(end_date.hour + end_date.minute / 60, working_hours_end)
                                      - max(start_date.hour + start_date.minute / 60, working_hours_start), 0)
        else:
            implementation_time = 0
    else:
        implementation_time = 0
        periods = end_date - start_date
        periods = periods.days - 1
        if periods > 0:
            date_list = pd.date_range(start_date.date() + dt.timedelta(days=1), periods=periods).to_pydatetime().tolist()
            date_list = [x for x in date_list if x.weekday() not in [5, 6] and x.date() not in holidays]

            implementation_time += working_day_in_hours * len(date_list)

        if start_date.weekday() not in [5, 6] and start_date.date() not in holidays:
            implementation_time += max(working_hours_end -
                                       max(start_date.hour + start_date.minute / 60, working_hours_start), 0)

        if end_date.weekday() not in [5, 6] and end_date.date() not in holidays:
            implementation_time += max(min(end_date.hour + end_date.minute / 60, working_hours_end)
                                       - working_hours_start, 0)

    row[2] = implementation_time

    return row


def main(n):
    print('iteration', n)

    start_time = time.time()
    num_of_rows = 10 ** n
    df = pd.DataFrame(columns=columns)

    names = [j for j in range(num_of_rows)]
    df['Name'] = names
    df.set_index('Name', inplace=True)

    start_dates = []
    end_dates = []

    for j in range(num_of_rows):
        start_date, end_date = get_random_date_range()
        start_dates.append(start_date)
        end_dates.append(end_date)

    df['Start Date'] = start_dates
    df['End Date'] = end_dates

    df.to_csv('data.csv', header=True)

    date_parser = lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    chunk_size = 10 ** 5
    for chunk in pd.read_csv('data.csv', chunksize=chunk_size, parse_dates=[1, 2], date_parser=date_parser):
        chunk.set_index('Name', inplace=True)
        chunk = chunk.apply(func=get_implementation_time, axis=1)
        chunk.to_csv('result.csv', mode='a', header=False)

    return time.time() - start_time  # return execution time


if __name__ == '__main__':
    execution_time_list = []
    r = range(1, 5)

    for i in r:
        if os.path.exists('result.csv'):
            os.remove('result.csv')
        execution_time_list.append(main(i))

    print('x:', [10 ** i for i in r])
    print('y:', execution_time_list)

    plt.plot([10 ** i for i in r], execution_time_list, color='#97dc91')
    plt.savefig("plot.png")
