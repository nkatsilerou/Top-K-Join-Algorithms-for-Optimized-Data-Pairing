#NEFELI-KATSILEROU 4385
import heapq
import time

# Initialize global variables
counter = 0
males_hash = {}
maxWeightMen = 0
currentWeightMen = 0
menViewCount = 0
females_hash = {}
maxWeightWomen = 0
currentWeightWomen = 0
womenViewCount = 0
max_heap = []
threshold = 0
results_generated = 0
currentLine = ""
maleLineGenerator = None
femaleLineGenerator = None
seen_pairs = set()

# Function to read sorted files alternately
def read_sorted_file1(file):
    with open(file, 'r') as fileReader:
        line = fileReader.readline().strip()
        while line:
            yield line
            line = fileReader.readline().strip()

def read_sorted_file2(file):
    with open(file, 'r') as fileReader:
        line = fileReader.readline().strip()
        while line:
            yield line
            line = fileReader.readline().strip()

# Function to extract relevant fields from a line
def extract_fields(line):
    fields = line.split(',')
    instance_weight = None
    age = None
    id = None

    try:
        age = int(fields[1])
        instance_weight = float(fields[25])

        # Check if the individual is married or a minor
        if fields[8].startswith(" Married") or age < 18: 
            return None, None, None
        
        id = fields[0]
        return id, instance_weight, age
    except (IndexError, ValueError):
        return None, None, None

def top_k_join(males_sorted, females_sorted, k):
    global males_hash, maxWeightMen, currentWeightMen, menViewCount
    global females_hash, maxWeightWomen, currentWeightWomen, womenViewCount
    global max_heap, threshold, results_generated, currentLine, maleLineGenerator, femaleLineGenerator, counter, seen_pairs
    
    while results_generated < k:
        if counter % 2 == 0:  # Process male
            try:
                currentLine = next(maleLineGenerator)
            except StopIteration:
                break
            counter += 1

            id, weight, age = extract_fields(currentLine)
            
            # Handle invalid data
            if weight is None or age is None:
                continue
            
            if menViewCount == 0:
                maxWeightMen = weight
                menViewCount = 1
            
            currentWeightMen = weight

            # Update max weight if a bigger one is found
            if currentWeightMen > maxWeightMen:
                maxWeightMen = currentWeightMen

            # Update threshold
            threshold = max(maxWeightMen + currentWeightWomen, currentWeightMen)

            # Update hash table
            males_hash.setdefault(age, []).append((weight, id))
            
            # Join with females of the same age
            if age in females_hash:
                for female_weight, female_record in females_hash[age]:
                    for male_weight, male_record in males_hash[age]:
                        total_weight = male_weight + female_weight
                        if total_weight >= threshold:
                            pair = (male_record, female_record)
                            if pair not in seen_pairs:
                                seen_pairs.add(pair)
                                heapq.heappush(max_heap, (-total_weight, (male_record, female_record), total_weight))
        else:  # Process female
            try:
                currentLine = next(femaleLineGenerator)
            except StopIteration:
                break
            counter += 1
            id, weight, age = extract_fields(currentLine)
            
            # Handle invalid data
            if weight is None or age is None:
                continue
            
            if womenViewCount == 0:
                maxWeightWomen = weight
                womenViewCount = 1
            
            currentWeightWomen = weight
            
            # Update max weight if a bigger one is found
            if currentWeightWomen > maxWeightWomen:
                maxWeightWomen = currentWeightWomen
            
            # Update threshold
            threshold = max(maxWeightMen + currentWeightWomen, currentWeightMen + maxWeightWomen)

            # Update hash table
            females_hash.setdefault(age, []).append((weight, id))
            
            # Join with males of the same age
            if age in males_hash:
                for female_weight, female_record in females_hash[age]:
                    for male_weight, male_record in males_hash[age]:
                        total_weight = male_weight + female_weight
                        if total_weight >= threshold:
                            pair = (male_record, female_record)
                            if pair not in seen_pairs:
                                seen_pairs.add(pair)
                                heapq.heappush(max_heap, (-total_weight, (male_record, female_record), total_weight))
        
        # Output pairs above threshold
        while max_heap and results_generated < k:
            score, (male_id, female_id), total_weight = heapq.heappop(max_heap)
            if -score >= threshold:
                yield f"{results_generated + 1}. pair: {male_id},{female_id} score: {total_weight:.2f}"
                results_generated += 1



K = int(input("Enter the value of K: "))
males_sorted = "males_sorted.txt"
females_sorted = "females_sorted.txt"

start_time = time.time()

maleLineGenerator = read_sorted_file1(males_sorted)
femaleLineGenerator = read_sorted_file2(females_sorted)
kjoin = top_k_join(males_sorted, females_sorted, K)


for result in kjoin:
    print(result)

end_time = time.time()
print("Execution time:", end_time - start_time, "seconds")
