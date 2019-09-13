# This code creates a Poll summary of the following:
# 1. total number of votes cast
# 2. complete list of candidates who received votes
# 3. percentage of votes each candidate won
# 4. total number of votes each candidate won
# 5. winner of election based on popular vote
#
# Outputs should print poll summary to terminal and export text file with results

import csv
# open csv file and save to data so that csv file can be closed
with open('election_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

# save votes in list from data
votes = []
for row in data[1:]: #column title offset: start list from index 1
    votes.append(row[2])

# 1. calculate total number of votes 
total_votes = len(votes)

# 2. complete list of candidates who received votes
candidates = set(votes)
candidates = list(candidates)

# 3. & 4. calculate number of votes, percentage of votes for each candidate who received votes
total_count_of_candidates = []
for candidate in candidates:
    candidate_count = votes.count(candidate)
    candidate_count_percentage = (candidate_count/total_votes*100)
    cand = [candidate, candidate_count_percentage, candidate_count]
    total_count_of_candidates.append(cand)

# 3-1. sort list in decending order (highest to lowest)
total_count_of_candidates.sort(key = lambda x: x[2], reverse = True)

# 5. determine winner
max_votes = 0
winner = ""
for cand in total_count_of_candidates:
    if (cand[2] > max_votes): 
        max_votes = cand[2]
        winner = cand[0]
    
# terminal output of election results
print("Election Results")
print("-----------------------------")
print(f"Total Votes: {total_votes}")
print("-----------------------------")
for cand in total_count_of_candidates: 
    print(f"{cand[0]}: {cand[1]:.3f}% ({cand[2]})")
print("-----------------------------")
print(f"Winner: {winner}")
print("-----------------------------")

# export Election Results to txt file
file = open("election_results.txt", 'w')
file.write('Election Results \n')
file.write('----------------------------------\n')
file.write('Total Votes: ' + str(total_votes) +'\n')
file.write('----------------------------------\n')
for cand in total_count_of_candidates: 
    file.write(str(cand[0]) + ': ' + str('%.3f' % cand[1]) + '% (' + str(cand[2]) + ') \n')
file.write('----------------------------------\n')
file.write('Winner: ' + str(winner) + '\n')
file.write('----------------------------------\n')
file.close()

