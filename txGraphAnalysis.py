# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#from plotnine import * # For ggplot
from statistics import mode
import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()

transactions = pd.read_csv("./transactions.csv")
# filling to_address that's entirely space (or empty) with NaN
transactions.replace(r'^\s*$', np.nan, inplace=True)
# replacing na values in to_address with No address
transactions["to_address"].fillna("No address", inplace = True)

to_addrs = transactions["to_address"].astype(str)
# Extracting all from_address
frm_addrs = transactions['from_address'].astype(str)

# For an overall analysis of all the addresses
unique_frm_addrs = set(frm_addrs)
unique_frm_addrs_list = list(unique_frm_addrs)   # For graph labeling

unique_to_addrs = set(transactions["to_address"]) - unique_frm_addrs
print(len(unique_to_addrs))


#print(set(frm_addrs)) # It prints all the unique addresses in the transaction data file
fixed_frm_addr = hex(0x3C55eA05Ba94839719AF636f78291bd1ce508882) # or input your own
#fixed_frm_addr = frm_addrs[0]

#values = transactions['value'].astype(str).astype(float)
#print(sum(values))
total_txs = []
addr_no = 0
for fixed_frm_addr in list(unique_frm_addrs):
    fixed_value = []
    fixed_to_addrs = []
    index = 0
    for frm_addr in transactions['from_address']:
        if frm_addr == fixed_frm_addr:
            fixed_value.append(float(transactions['value'][index]))
            fixed_to_addrs.append(transactions['to_address'][index])
            G.add_edge(fixed_frm_addr, transactions['to_address'][index])
        index+=1
    #most_to_addr = mode(fixed_to_addrs)
    total_txs.append(len(fixed_value))
    addr_no+=1
    print(str(addr_no) + ".")
    print("from address: " + fixed_frm_addr)
    most_to_addr = max(fixed_to_addrs, key=fixed_to_addrs.count)
    print("Total number of transactions found: " + str(len(fixed_value)))
    print("Total value sent: " + str(sum(fixed_value)))
    print("Most used to_address: " + str(most_to_addr) + " by: " + str(fixed_frm_addr))
    print("Total value sent by: " + str(fixed_frm_addr) + " to: " + str(most_to_addr) + " is: " + str(sum(fixed_value)))
    print("======================================================")

print("Total transactions across all accounts: " + str(sum(total_txs)))

# Extracting inter-contract interaction
for fixed_to_addr in list(unique_to_addrs):
    index = 0
    for to_addr in transactions['from_address']:
        if to_addr == fixed_to_addr:
            G.add_edge(fixed_to_addr, transactions['to_address'][index])
        index+=1

#print(transactions["to_address"])

#print(len(fixed_value))
#print(len(fixed_to_addrs))
#print(fixed_value)
#print(fixed_to_addrs)
# Most used to_address by our fixed_frm_addr
#################################################################################################

################
#Graph analysis#
################

pos = nx.spring_layout(G)
print(len(set(frm_addrs)))
print(len(set(to_addrs)))
print(len(set(frm_addrs).intersection(set(to_addrs))))

contract_addresses = unique_to_addrs-unique_frm_addrs

# Inter-account edges
inter_account_edges = [(u, v) for u, v in G.edges() if (u in unique_frm_addrs and v in unique_frm_addrs)]
#print(inter_account_edges)
# Inter account-contract
account_contract_edges = [(u, v) for u, v in G.edges() if not ((u, v) in inter_account_edges)]
# Contract creation edges
contract_creation_edges = [(u, v) for u, v in G.edges() if v=="No address" or u=="No address"]
# Inter-contract interaction
inter_contract_edges = [(u, v) for u, v in G.edges() if (u in contract_addresses and v in contract_addresses)]
#print(inter_contract_edges)
# Nodes with "No address"
no_address_nodes = [n for n in G.nodes() if n=="No address"]


#print(inter_account_edges)

#G.add_nodes_from(list(set(frm_addrs)))
nx.draw_networkx_nodes(G, pos, nodelist=unique_frm_addrs, node_color="red")
nx.draw_networkx_nodes(G, pos, nodelist=contract_addresses, node_size=50,  node_color="blue")
#nx.draw_networkx_nodes(G, pos, nodelist=no_address_nodes, node_color="green")
#nx.draw_networkx_edges(G, pos, edgelist=inter_account_edges, width=2, edge_color="red")
#nx.draw_networkx_edges(G, pos, edgelist=account_contract_edges, edge_color="blue")
#nx.draw_networkx_edges(G, pos, edgelist=inter_contract_edges, edge_color="green")
#nx.draw_networkx_edges(G, pos, edgelist=contract_creation_edges, edge_color="green")
print(len(G.nodes()))
print(G.degree(set(frm_addrs)))

# Labeling frm_addrs nodes with their degrees
labels = {}

index = 0
for i in range(0, len(unique_frm_addrs_list)):
    labels[unique_frm_addrs_list[i]] = G.degree[unique_frm_addrs_list[i]]

nx.draw_networkx_labels(G, pos, labels, font_size=14)
#nx.draw(G, with_labels=False, font_weight='bold')
plt.savefig("allTransactionNodes.pdf")
plt.show()


################################################################################################
