import sys

total = 0
count = 0

for line in sys.stdin:
    try:
        _, value = line.strip().split("\t")
        total += float(value)
        count += 1
    except:
        continue

if count > 0:
    print(f"Average age: {total / count:.2f}")
else:
    print("No valid ages found")