# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from statistics import *
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


G = nx.DiGraph()

###################################################################################################################################
# Data reading/cleaning
###################################################################################################################################

traces = pd.read_csv("./traces.csv")
# filling to_address that's entirely space (or empty) with NaN
traces.replace(r'^\s*$', np.nan, inplace=True)
# replacing na values in to_address with No address
traces.fillna(0, inplace = True)

frm_addrs = traces["from_address"].astype(str)
unique_frm_addrs = set(frm_addrs)

values = traces["value"].astype(float)

to_addrs = traces["to_address"].astype(str)
unique_to_addrs = set(to_addrs)
#print(unique_to_addrs)

trace_type = traces["trace_type"].astype(str)
print(Counter(trace_type).keys())
print(Counter(trace_type).values())



###################################################################################################################################
# Analysing contract creations
###################################################################################################################################

contract_creators = []
contract_addrs_created = []
total_creations = 0
for fixed_frm_addr in list(unique_frm_addrs):
    contract_addrs = []
    index = 0
    for frm_addr in frm_addrs:
        if fixed_frm_addr == frm_addr and trace_type[index] == "create":
            contract_addrs.append(to_addrs[index])
            contract_creators.append(fixed_frm_addr)
            G.add_edge(fixed_frm_addr, to_addrs[index])
        index+=1
    total_creations += len(contract_addrs)
    contract_addrs_created.extend(contract_addrs)
    #print("Address " + fixed_frm_addr + " created " + str(len(contract_addrs)) + " contracts")

print("Checking total creations through the list: " + str(len(contract_addrs_created)))
print(len(set(contract_addrs_created)))
print("Creation calls: " + str(total_creations))
print("Contract creators: " + str(len(set(contract_creators))))



###################################################################################################################################
# Analysing contract calls - without value + value
###################################################################################################################################

contract_callers = []
contract_addrs_called = []
total_calls = 0
for fixed_frm_addr in list(unique_frm_addrs):
    contract_addrs = []
    index = 0
    for frm_addr in frm_addrs:
        if fixed_frm_addr == frm_addr and trace_type[index] == "call":
            contract_addrs.append(to_addrs[index])
            contract_callers.append(fixed_frm_addr)
            G.add_edge(fixed_frm_addr, to_addrs[index])
        index+=1
    total_calls += len(contract_addrs)
    contract_addrs_called.extend(contract_addrs)
    #print("Address " + fixed_frm_addr + " called " + str(len(contract_addrs)) + " contracts")

print("Checking total calls through the list: " +str(len(contract_addrs_called)))
print("Total calls: " + str(total_calls))
print("Contractc callers: " +  str(len(set(contract_callers))))


###################################################################################################################################
# Analysing contract calls - value
###################################################################################################################################

contract_value_callers = []
contract_addrs_value_called = []
total_calls = 0
for fixed_frm_addr in list(unique_frm_addrs):
    contract_addrs = []
    index = 0
    for frm_addr in frm_addrs:
        if fixed_frm_addr == frm_addr and trace_type[index] == "call" and values[index] > 0:
            contract_addrs.append(to_addrs[index])
            contract_value_callers.append(fixed_frm_addr)
            G.add_edge(fixed_frm_addr, to_addrs[index])
        index+=1
    total_calls += len(contract_addrs)
    contract_addrs_value_called.extend(contract_addrs)
    #print("Address " + fixed_frm_addr + " called " + str(len(contract_addrs)) + " contracts")

i = 0
for value in values:
    if value > 0:
        i += 1
print("Actual value calls: " + str(i))
print("Checking total value calls through the list: " + str(len(contract_addrs_value_called)))
print("Total value calls: " + str(total_calls))
print("Contractc value callers: " +  str(len(set(contract_value_callers))))


###################################################################################################################################
# Graph generation
###################################################################################################################################



G.add_nodes_from(unique_to_addrs)
G.add_nodes_from(unique_frm_addrs)

pos = nx.spring_layout(G, k=0.7, iterations=20)

# Creation edges #########################################
creation_edges = [(u, v) for u, v in G.edges() if (u in contract_creators and v in set(contract_addrs_created))]
# Call edges #############################################
called_edges = [(u, v) for u, v in G.edges() if (u in contract_callers and v in set(contract_addrs_called))]
# Call edges value #######################################
called_value_edges = [(u, v) for u, v in G.edges() if (u in contract_value_callers and v in set(contract_addrs_value_called))]


# Drawing nodes ##########################################
nx.draw_networkx_nodes(G, pos, nodelist=set(contract_creators), node_color="red")
nx.draw_networkx_nodes(G, pos, nodelist=unique_to_addrs-set(contract_creators), node_size=40, node_color="blue")

#print(set(contract_creators).intersection(unique_to_addrs))

# Drawing edges ##########################################
#nx.draw_networkx_edges(G, pos, edgelist=creation_edges, width=2, edge_color="green") # To created contracts from contract_creators
#nx.draw_networkx_edges(G, pos, edgelist=called_edges, width=1, edge_color="blue") # To contract calls from contract_creators
#nx.draw_networkx_edges(G, pos, edgelist=called_value_edges, width=1, edge_color="red") # To contract calls from contract_creators

# Labeling frm_addrs nodes with their degrees ############
labels = {}
contract_creators_list = list(contract_creators)
index = 0
for i in range(0, len(contract_creators_list)):
    labels[contract_creators_list[i]] = G.degree[contract_creators_list[i]]

nx.draw_networkx_labels(G, pos, labels, font_size=14)


plt.axis("off")
plt.savefig("allTraceNodes.pdf");
plt.show()
