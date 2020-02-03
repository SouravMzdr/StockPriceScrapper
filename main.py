#Program by SOURAV MAZUMDAR
#Program to get back stock prices from Yahoo Finance and save them to a .csv file

#Import necessary modules
import requests
import bs4
import sys
import time
from _datetime import datetime
import csv


#Set the maximum retries allowed in case of network slowdown or connection error
MAX_RETRIES = 10

def getQuote(symbol):  #Function fetches the quotes and writes to csv file

    #set the initial retry count as 1 after every successful connection
    retries = 1

    #Marker for Connection status
    success = False

    #Check for connection error

    #-------------------------------------------------------------------------------------------------------
    #This exception handling method allows the program to not shutdown abruptly incase of any network error
    #-------------------------------------------------------------------------------------------------------

    while not success:
        try:

            # ticker symbol is taken from the user adn passed to the function by the driver code
            #make HTTP request to get the webpage from Yahoo finance
            r = requests.get("https://in.finance.yahoo.com/quote/" + symbol + ".NS?p=INFY.NS&.tsrc=fin-srch")
            success = True                  #If successful connection is establised then set success as true

        except Exception as e:
            #if connection error then wait for initially 30 secs and try again
            #the waiting is incremented with each failed try

            #Exit if max retires is exceeded
            if retries > MAX_RETRIES:
                print("MAXIMUM ALLOWED RETRIES EXCEEDED!!CHECK NETWORK CONNECTION ADN TRY AGAIN. EXITING.......")
                sys.exit(1)

            wait = retries * 30;
            print ('Error! Waiting %s secs and re-trying...' % wait)
            sys.stdout.flush()
            time.sleep(wait)
            retries += 1
    #end of connection error eexception handling

    #Parse the succesfully loaded webpage
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    #Declare the value to be stored as a empty list
    value = []


    #Exception handling to check for invalid ticker
    try:
        price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    except IndexError:
        print("No stock found")         #Incase of invalid ticker symbol notify user and exit gracefully
        sys.exit(1)


    #Get current timestamp accurate to the second
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value.append(timestamp)         #Keep the timestamp for the currently fetched result as the first field
    value.append(price)             #Keep the current price as the second field

    #Parse table for additional information
    tables = soup.findChildren('table')

    my_table = tables[0]

    rows = my_table.findChildren(['tr'])

    #Loop over each row of the table
    for row in rows:
        cells = row.findChildren('td')
        value.append(cells[1].string)

    # print(value) #Used for debugging purpose

    writer.writerow(value)
    print('Value recorded sucessfully at - '+ timestamp)

    #Wait to run again after set interval
    time.sleep(interval*60)


#----------------------------------------
#DRIVER CODE
#----------------------------------------


#Get the ticker symbol from the user
symbol = input("Enter Symbol:")

#Ask User for custom time interval or else set to 30mins
interval = input("Enter time interval required(Press Enter to default to 30 mins: ")

if interval is not '':
    interval = int(interval)
else:
    interval = 30

#Create a .csv file to record the data
fd = open(symbol.lower() + '.csv', 'a', newline="")
writer = csv.writer(fd, dialect="excel")

#Set the first row as the field heading
writer.writerow(['Timestamp','Curr price','Previous close','Open','Bid','Ask',"Day's range", '52-week range','Volume','Avg volumere'])


print("Data recording process started!!\n This porogram will keep running unless explicitly closed \nPress ctrl+c to close")


#Start infinte loop
while True:
    try:
        getQuote(symbol)
    except KeyboardInterrupt:               #Ask for  user interrupt to close the program and exit gracefully
        print("Program closed successfully. \n Data saved in file "+ symbol+".csv")
        break


#End of program