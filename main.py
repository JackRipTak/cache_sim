import argparse


class CacheSimulator:
    def __init__(self, cache_size, cache_associativity, cache_block_size, trace_file):
        self.cache_size = cache_size
        self.cache_associativity = cache_associativity
        self.cache_block_size = cache_block_size
        self.trace_file = trace_file
        self.cache_lines = cache_size // (cache_associativity * cache_block_size)
        self.cache = [[None] * cache_associativity for _ in range(self.cache_lines)]
        self.access_count = 0
        self.miss_count = 0

    def simulate(self):
        with open(self.trace_file, 'r') as file:
            for line in file:
                access_type, address, data = line.strip().split()
                self.access_count += 1
                if access_type == '0':
                    if not self.cache_lookup(address):
                        self.miss_count += 1
                        self.cache_load(address)
                elif access_type == '1':
                    if not self.cache_lookup(address):
                        self.miss_count += 1
                        self.cache_load(address)
                    self.cache_store(address, data)

    def cache_lookup(self, address):
        tag, index, _ = self.cache_address_decode(address)
        for i in range(self.cache_associativity):
            if self.cache[index][i] == tag:
                return True
        return False

    def cache_load(self, address):
        tag, index, _ = self.cache_address_decode(address)
        for i in range(self.cache_associativity):
            if self.cache[index][i] is None:
                self.cache[index][i] = tag
                return
        for i in range(1, self.cache_associativity):
            self.cache[index][i - 1] = self.cache[index][i]
        self.cache[index][self.cache_associativity - 1] = tag

    def cache_store(self, address, data):
        tag, index, offset = self.cache_address_decode(address)
        for i in range(self.cache_associativity):
            if self.cache[index][i] == tag:
                # Update cache line
                self.cache[index][i] = tag
                break

    def cache_address_decode(self, address):
        address = int(address, 16)
        offset_bit = self.log2(self.cache_block_size)
        index_bit = self.log2(self.cache_lines)
        tag_bit = 32 - offset_bit - index_bit

        offset_mask = (1 << offset_bit) - 1
        index_mask = ((1 << index_bit) - 1) << offset_bit
        tag_mask = ((1 << tag_bit) - 1) << (offset_bit + index_bit)

        offset = address & offset_mask
        index = (address & index_mask) >> offset_bit
        tag = (address & tag_mask) >> (offset_bit + index_bit)

        return tag, index, offset

    @staticmethod
    def log2(x):
        return (x - 1).bit_length()

    def calculate_miss_rate(self):
        miss_rate = self.miss_count / self.access_count
        return miss_rate


def main():
    trace_files = ['1.din', '2.din', '3.din', '4.din']
    cache_sizes = [8 * 1024, 16 * 1024, 32 * 1024, 64 * 1024]
    block_sizes = [16, 32, 64, 128]
    associativities = [1, 2, 4, 8]

    for trace_file in trace_files:
        print(trace_file)
        for cache_size in cache_sizes:
            for block_size in block_sizes:
                for associativity in associativities:
                    simulator = CacheSimulator(cache_size, associativity, block_size, trace_file)
                    simulator.simulate()

                    print(f"{cache_size} {block_size} {associativity} {simulator.access_count} {simulator.miss_count} {simulator.calculate_miss_rate()}")

if __name__ == '__main__':
    main()
