import os
os.chdir('C:/Users/joanv/OneDrive/Escritorio/files_datacamp/')


import requests

for i in range(1,13):
    print(i)
    if i <10:
        csv_url =  'https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2020-0{}.csv'.format(i)
        file_name = 'green_tripdata_2020-0{}.csv'.format(i)
    else:
        csv_url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2020-{}.csv'.format(i)
        file_name = 'green_tripdata_2020-{}.csv'.format(i)
    
    req = requests.get(csv_url)
    url_content = req.content
    
    csv_file = open(file_name, 'wb')
    
    csv_file.write(url_content)
    csv_file.close()
