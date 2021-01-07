* The code in **transaction.py** is to analyse the transaction data of my blockchain on kaggle notebook.

* Data collected using `python3 -m ethereumetl export_blocks_and_transactions -s 0 -e 6397 --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri http://localhost:8545` while my blockchain is running.

* All the most basic needed `ethereumetl` commands
```
 1886  python3 -m ethereumetl
 1888  python3 -m ethereumetl export_all -s 0 -e 6000 -b 500 -p file://home/ali/ethereumDocker_attempt2/node1/geth.ipc -o output
 1889  python3 -m ethereumetl export_blocks_and_transactions -s 0 -e 6000 --blocks-output blocks.csv --transaction-output transactions.csv --provider-uri http://localhost:8545
 1890  python3 -m ethereumetl export_blocks_and_transactions -s 0 -e 6000 --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri http://localhost:8545
 1903  python3 -m ethereumetl export_blocks_and_transactions -s 0 -e 6397 --blocks-output blocks.csv --transactions-output transactions.csv --provider-uri http://localhost:8545
 1906  python3 -m ethereumetl export_traces -s 0 -e 6397 --blocks-output traces.csv --provider-uri http://localhost:8545
 1910  python3 -m ethereumetl export_traces -s 0 -e 6397 --blocks-output traces.csv --provider-uri http://localhost:8545
 1911  python3 -m ethereumetl export_traces -s 0 -e 6397 --provider-uri http://localhost:8545 --output pythonBlockChainDataAnalysis/traces.csv
 1913  python3 -m ethereumetl export_traces -s 0 -e 6397 --provider-uri http://localhost:8545 --output pythonBlockChainDataAnalysis/traces.csv
 1914  python3 -m ethereumetl export_traces -s 0 -e 6397 --provider-uri file://home/ali/ethereumDocker_attempt2/node1/geth.ipc --output pythonBlockChainDataAnalysis/traces.csv
 1918  python3 -m ethereumetl export_geth_traces -s 0 -e 6397 --provider-uri file://home/ali/ethereumDocker_attempt2/node1/geth.ipc --batch-size 100 --output pythonBlockChainDataAnalysis/traces.json
 1920  python3 -m ethereumetl export_geth_traces -s 0 -e 6397 --provider-uri http://localhost:8545 --batch-size 100 --output pythonBlockChainDataAnalysis/traces.json
 1926  python3 -m ethereumetl extract_geth_traces --input traces.json  --output traces.csv
 1930  python3 -m ethereumetl extract_csv_column --input transactions.csv --column hash --output transaction_hashes.txt
 1933  python3 -m ethereumetl export_receipts_and_logs --transaction-hashes transaction_hashes.txt --provider-uri http://localhost:8545 --receipts-output tx_receipts.csv --logs-output logs.csv
 1935  python3 -m ethereumetl extract_csv_column --input tx_receipts.csv  --column contract_address --output contract_addresses.txt
 1938  python3 -m ethereumetl export_contracts --contract-addresses contract_addresses.txt --provider-uri http://localhost:8545 --output contracts.csv

```
