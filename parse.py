#!/usr/bin/env python
import argparse
import csv
import sys
from decimal import Decimal
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("csv_file", help="input .csv file", type=argparse.FileType('r', encoding='utf16'))
args = parser.parse_args()
reader = csv.reader(args.csv_file)

header = True
default = lambda: Decimal('0') 
data = defaultdict(default)
shipping = Decimal('0')
paypal_fees = Decimal('0')
pending_sales = False

for row in reader:
    if header:
        try:
            header = False
            net_amount_column = row.index('net amount')
            catalog_number_column = row.index('catalog number')
            shipping_column = row.index('shipping')
            item_type_column = row.index('item type')
            fee_type_column = row.index('fee type')
            transaction_fee_column = row.index('transaction fee')
        except ValueError:
            print("Error finding correct data in .csv files")
            sys.exit()
    else:
        catalog_number = row[catalog_number_column]
        shipping_amount = row[shipping_column]
        net_amount = row[net_amount_column]
        item_type = row[item_type_column]
        fee_type = row[fee_type_column]
        transaction_fee = row[transaction_fee_column]

        if catalog_number:
            if item_type == 'pending sale':
                pending_sales = True
            elif net_amount:
                data[catalog_number] += Decimal(net_amount)
                if shipping_amount:
                    shipping += Decimal(shipping_amount)

        elif fee_type == 'transfer':
            if transaction_fee:
                paypal_fees += Decimal(transaction_fee)

for k in data:
    print("{}\n    ${}\n".format(k, data[k]))

print("Shipping\n    ${}\n".format(shipping))
print("Paypal Fees\n    ${}\n".format(paypal_fees))
print("Pending Sales!!!" if pending_sales else "")

