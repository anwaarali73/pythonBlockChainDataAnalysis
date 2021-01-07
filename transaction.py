# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from plotnine import * # For ggplot
from statistics import mode


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#import os
#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

transactions = pd.read_csv("../input/ethereum-transactions/transactions.csv")
# filling to_address that's entirely space (or empty) with NaN
transactions.replace(r'^\s*$', np.nan, inplace=True)
# replacing na values in to_address with No address 
transactions["to_address"].fillna("No address", inplace = True)
to_addrs = transactions["to_address"]
# Extracting all from_address
frm_addrs = transactions['from_address'].astype(str)

# For an overall analysis of all the addresses
unique_frm_addrs = set(frm_addrs)
#print(set(frm_addrs)) # It prints all the unique addresses in the transaction data file
fixed_frm_addr = hex(0x3C55eA05Ba94839719AF636f78291bd1ce508882) # or input your own
#fixed_frm_addr = frm_addrs[0]

#values = transactions['value'].astype(str).astype(float)
#print(sum(values))
addr_no = 0
for fixed_frm_addr in unique_frm_addrs:
    fixed_value = []
    fixed_to_addrs = []
    index = 0
    for frm_addr in transactions['from_address']:
        if frm_addr == fixed_frm_addr:
            fixed_value.append(float(transactions['value'][index]))
            fixed_to_addrs.append(transactions['to_address'][index])
        index+=1
    #most_to_addr = mode(fixed_to_addrs)
    addr_no+=1
    print(str(addr_no) + ".")
    print("from address: " + fixed_frm_addr)
    most_to_addr = max(fixed_to_addrs, key=fixed_to_addrs.count)
    print("Total number of transactions found: " + str(len(fixed_value)))
    print("Total value sent: " + str(sum(fixed_value)))
    print("Most used to_address: " + str(most_to_addr) + " by: " + str(fixed_frm_addr))
    print("Total value sent by: " + str(fixed_frm_addr) + " to: " + str(most_to_addr) + " is: " + str(sum(fixed_value)))
    print("======================================================")
        
#print(transactions["to_address"])
        
#print(len(fixed_value))
#print(len(fixed_to_addrs))
#print(fixed_value)
#print(fixed_to_addrs)
# Most used to_address by our fixed_frm_addr

    
