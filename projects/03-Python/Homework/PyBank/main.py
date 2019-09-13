# This code creates a Financial Analysis of the following:
# 1. total number of months of dataset
# 2. net total amount of profit/loss
# 3. average profits/losses
# 4. greatest increase in profits (date and amount)
# 5. greatest decrease in losses (date and amount)
#
# Outputs should print analysis to terminal and export text file with results

import csv

# open csv file and save to data so that csv file can be closed 

with open('budget_data.csv', 'r', newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

# initializing lists: dates, values, values_offset (for month to month change calculation), and change_values (change of gains/losses per month)
dates = []
values = []
values_offset = []
change_values = []

# divide data into list of dates, profits/losses (as variable: values), values_offset and calculate monthly change of values 
for row in data[1:]: #column title offset: start list from index 1
    dates.append(row[0])
    values.append(int(row[1]))

for valueRow in values[1:]: #offset of 1 value in the beginning to see month to month change of gain/loss
    values_offset.append(valueRow)

change_values = [(valuesOffset-values) for values,valuesOffset in zip(values, values_offset)]

# 1. calculates total number of months of the dataset
total_months = len(dates) 

# 2. calculates net total amount of profit/loss 
net_total = 0
for row in values:
    net_total += int(row)

# 3. average of changes in profit/loss
net_avg_change = 0
for change in change_values:
    net_avg_change += change
average_profitLoss = net_avg_change/(len(change_values))

# 4. greatest increase in profits (date/amount)
greatest_profits = max(change_values)
greatest_profits_date = dates[change_values.index(greatest_profits)+1] # offset of 1 to account for first value of change_values starting from index 0 

# 5. greatest decrease in losses (date/amount)
greatest_losses = min(change_values)
greatest_losses_date = dates[change_values.index(greatest_losses)+1] # offset of 1 to account for first value of change_values starting from index 0 

# 6. print Financial Analysis 
print("Financial Analysis")
print("----------------------------------")
print(f"Total_months: {total_months}")
print(f"Total: ${net_total}")
print(f"Average Change: ${round(average_profitLoss, 2)}")
print(f"Greatest Increase in Profits: {greatest_profits_date} (${greatest_profits})")
print(f"Greatest Decrease in Losses: {greatest_losses_date} (${greatest_losses})")

# export Financial Analysis results to txt file
file = open("financial_analysis.txt", 'w')
file.write('Financial Analysis \n')
file.write('----------------------------------\n')
file.write('Total months: ' + str(total_months) +'\n')
file.write('Total: $' + str(net_total)+'\n')
file.write('Average Change: $' + str(round(average_profitLoss, 2))+'\n')
file.write('Greatest Increase in Profits: ' + str(greatest_profits_date) + ' ($' + str(greatest_profits) + ')\n')
file.write('Greatest Decrease in Losses: ' + str(greatest_losses_date) +  ' ($' + str(greatest_losses) + ')\n')
file.close()