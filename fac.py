import requests
from bs4 import BeautifulSoup
import datetime
from csv import writer
import time
import pandas as pd
import matplotlib.pyplot as plt





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



def plot(column='UTFG'):
    df = pd.read_csv('./info.csv')
    df['time'] = (df['hour']*100)+df['minute']
    column_data = df[column]

    column_x_label = df['time']

    plt.figure(figsize=(10, 6))
    plt.plot(column_data, marker='o')

    # Replace x-axis tick labels with values from x_labels_column_name
    plt.xticks(ticks=range(len(column_x_label)), labels=column_x_label, rotation=45, ha='right')

    # Set title and labels
    #plt.title(f'Plot of {column_data}')
    #plt.xlabel(column_x_label)
    #plt.ylabel(column_data)
    plt.grid(True)
    plt.tight_layout()
    plt.show()



if __name__=="__main__":
    #plot(column='USCG')

    #time.sleep(10000)
    while datetime.datetime.now().hour<7:
         time.sleep(60)
    #run loop
    while datetime.datetime.now().hour<=22:
        if(datetime.datetime.now().minute%5==0):        
            append_to_csv()
            time.sleep(240)


