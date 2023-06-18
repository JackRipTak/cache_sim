import matplotlib.pyplot as plt

fixed_cache_size = 8192  # 固定的缓存大小（bytes）
fixed_block_size = 16  # 固定的块大小（bytes）

data = []
with open('data.txt', 'r') as file:
    for line in file:
        line = line.strip().split(' ')
        cache_size = int(line[0])
        block_size = int(line[1])
        associativity = int(line[2])
        miss_rate = float(line[5])

        if cache_size == fixed_cache_size and block_size == fixed_block_size:
            data.append((associativity, miss_rate))

associativities = [d[0] for d in data]
miss_rates = [d[1] for d in data]

plt.figure(figsize=(8, 6))
plt.scatter(associativities, miss_rates, c='blue')
plt.xlabel('Associativity')
plt.ylabel('Miss Rate')
plt.title('Miss Rate vs. Associativity (Cache Size: 8192B, Block Size: 16B)')
plt.grid(True)
plt.show()
