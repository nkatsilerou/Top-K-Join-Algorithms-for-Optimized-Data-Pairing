#NEFELI-ELENI KATSILEROU 4385
import heapq
import time

# Function to read sorted files
def read_sorted_file(file):
    with open(file, 'r') as fileReader:
        line = fileReader.readline().strip()
        while line:
            yield line
            line = fileReader.readline().strip()

# # Function to extract relevant fields from a line
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

# Function to implement the alternative top-k join algorithm
def alternative_top_k_join(males_sorted, females_sorted, k):
    males_hash = {}
    min_heap = []

    # Read the males_sorted file and build the hash table
    for line in read_sorted_file(males_sorted):
        id, weight, age = extract_fields(line)
       
        if weight is None or age is None:
            continue

        if age not in males_hash:
            males_hash[age] = []
        males_hash[age].append((weight, id))

    # Read the females_sorted file and perform the join
    for line in read_sorted_file(females_sorted):
        id, weight, age = extract_fields(line)

        if weight is None or age is None:
            continue

        if age in males_hash:
            for male_weight, male_id in males_hash[age]:
                total_weight = male_weight + weight
                if len(min_heap) < k:
                    heapq.heappush(min_heap, (total_weight, (male_id, id)))
                else:
                    if total_weight > min_heap[0][0]:
                        heapq.heappushpop(min_heap, (total_weight, (male_id, id)))

    # Extract the top K pairs from the min-heap
    results = []
    while min_heap:
        total_weight, (male_id, female_id) = heapq.heappop(min_heap)
        results.append((total_weight, male_id, female_id))
    results.sort(reverse=True)  # Sort the results by weight in descending order

    return results


K = int(input("Enter the value of K: "))
males_sorted = "males_sorted.txt"
females_sorted = "females_sorted.txt"

start_time = time.time()

top_k_pairs = alternative_top_k_join(males_sorted, females_sorted, K)

for i, (total_weight, male_id, female_id) in enumerate(top_k_pairs, 1):
    print(f"{i}. pair: {male_id},{female_id} score: {total_weight:.2f}")

end_time = time.time()
print("Execution time:", end_time - start_time, "seconds")
