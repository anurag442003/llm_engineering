
#include <iostream>
#include <vector>
#include <limits> // Required for numeric_limits
#include <chrono>


using namespace std;
using namespace std::chrono;


unsigned long long lcg(unsigned long long seed, unsigned long long a = 1664525, unsigned long long c = 1013904223, unsigned long long m = 4294967296ULL) {
    return (a * seed + c) % m;
}

long long max_subarray_sum(int n, unsigned long long seed, long long min_val, long long max_val) {
    vector<long long> random_numbers(n);
    unsigned long long current_seed = seed;
    for (int i = 0; i < n; ++i) {
        current_seed = lcg(current_seed);
        random_numbers[i] = (current_seed % (max_val - min_val + 1)) + min_val;
    }

    long long max_sum = numeric_limits<long long>::min();
    for (int i = 0; i < n; ++i) {
        long long current_sum = 0;
        for (int j = i; j < n; ++j) {
            current_sum += random_numbers[j];
            if (current_sum > max_sum) {
                max_sum = current_sum;
            }
        }
    }
    return max_sum;
}

long long total_max_subarray_sum(int n, unsigned long long initial_seed, long long min_val, long long max_val) {
    long long total_sum = 0;
    unsigned long long current_seed = initial_seed;
    for (int i = 0; i < 20; ++i) {
        current_seed = lcg(current_seed);
        total_sum += max_subarray_sum(n, current_seed, min_val, max_val);
    }
    return total_sum;
}

int main() {
    int n = 10000;
    unsigned long long initial_seed = 42;
    long long min_val = -10;
    long long max_val = 10;

    auto start = high_resolution_clock::now();
    long long result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    cout << "Total Maximum Subarray Sum (20 runs): " << result << endl;
    cout << "Execution Time: " << (double)duration.count() / 1000000 << " seconds" << endl;

    return 0;
}
