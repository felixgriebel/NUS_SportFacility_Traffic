import requests
from bs4 import BeautifulSoup
import datetime
from csv import writer
import time
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter





def get_numbers():
    response = requests.get("https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/capacity")
    soup = BeautifulSoup(response.text, 'html.parser')
    swimming_pools = soup.find_all('div', class_='swimbox')
    gyms = soup.find_all('div', class_='gymbox')
    value_list = []
    for box in swimming_pools:
            traffic = box.find('b').text.strip()
            value_list.append(traffic.split('/')[0])
    for box in gyms:
            traffic = box.find('b').text.strip()
            value_list.append(traffic.split('/')[0])
    return value_list

def append_to_csv():
    newrow=[]
    newrow.append(datetime.datetime.now().day)
    newrow.append(datetime.datetime.now().hour)
    newrow.append(datetime.datetime.now().minute)
    curr = get_numbers()
    for i in curr:
        newrow.append(i)
    with open('./info.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(newrow)
        f_object.close()
    print('app')


def plot(columns=['UTFG'], dates=[], avg=False, smooth=False):
    windows_size = 6
    poly = 3
    df = pd.read_csv('./info.csv')
    df['time_in_minutes'] = df['hour'] * 60 + df['minute']
    df['date'] = df['date'].astype(int)
    if dates:
        df = df[df['date'].isin(dates)]
    if df.empty:
        print("No data found for the specified dates.")
        return
    num_columns = len(columns)
    fig, axes = plt.subplots(num_columns, 1, figsize=(12, 6 * num_columns), sharex=True)
    if num_columns == 1:
        axes = [axes]  # Make axes iterable even if there's only one column
    for idx, column in enumerate(columns):
        ax = axes[idx]    
        if avg:
            df_avg = df.groupby('time_in_minutes')[column].mean().reset_index()
            df_avg = df_avg.sort_values(by='time_in_minutes')
            
            x = df_avg['time_in_minutes']
            y = df_avg[column]
            
            if smooth:
                y = savgol_filter(y, window_length=windows_size, polyorder=poly)
            ax.plot(x, y, label=f'Average of {column}')
            ax.set_title(f'Average of {column} over time for specified dates')
        else:
            unique_dates = sorted(df['date'].unique())
            for date in unique_dates:
                df_date = df[df['date'] == date]
                df_date = df_date.sort_values(by='time_in_minutes')
                x = df_date['time_in_minutes']
                y = df_date[column]
                if smooth:
                    y = savgol_filter(y, window_length=windows_size, polyorder=poly)
                ax.plot(x, y, label=f'Day {date}')
            ax.set_title(f'Plot of {column} over time for specified dates')
        ax.set_ylabel(column)
        ax.legend()
        ax.grid(True)
    min_time = df['time_in_minutes'].min()
    max_time = df['time_in_minutes'].max()
    x_ticks = range(int(min_time), int(max_time) + 1, 30)  # Every 30 minutes
    x_labels = [f"{t // 60:02d}:{t % 60:02d}" for t in x_ticks]
    axes[-1].set_xticks(x_ticks)
    axes[-1].set_xticklabels(x_labels, rotation=45, ha='right')
    axes[-1].set_xlabel('Time')
    plt.tight_layout()
    plt.show()


def clean_csv():
    df = pd.read_csv('./info.csv')
    print(len(df))
    df_filtered = df[~((df['hour'] >= 22) & (df['minute'] > 0))]
    print(len(df_filtered))
    df_filtered.to_csv('./filtered_info.csv', index=False)
    unique_values = df['date'].unique()
    print(len(unique_values))


if __name__=="__main__":
    #plot(column='USCG')
    #clean_csv()
    
    plot(columns=['KRSP'],dates=[20,27,4], avg=False, smooth=False)
    # while datetime.datetime.now().hour<7:
    #      time.sleep(60)
    # #run loop
    # while datetime.datetime.now().hour<=22:
    #     if(datetime.datetime.now().minute%5==0):        
    #         append_to_csv()
    #         if(datetime.datetime.now().hour==22):
    #             break
    #         time.sleep(240)


