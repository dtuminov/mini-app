# collections
from collections import Counter


async def find_duplicates(lst):
	counter = Counter(lst)
	
	duplicates = []
	for item, count in counter.items():
		if count > 1:
			duplicates.extend([item] * (count - 1))

	return duplicates
