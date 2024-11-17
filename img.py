#NEFELI-ELENI KATSILEROU 4385
import matplotlib.pyplot as plt

K = [1, 2, 5, 10, 20, 50, 100]
time_topKjoinA = [0.00449919, 0.00727248, 0.02379965, 0.12327241, 0.75655746, 6.51951479, 29.14399242]
time_topKjoinB = [2.82808113, 2.812684059, 2.82465076, 2.81967997, 2.82686519, 2.95955322, 2.9318366]

plt.figure(figsize=(12, 8))

plt.plot(K, time_topKjoinA, 'r-', marker='o', label='topKjoinA')
plt.plot(K, time_topKjoinB, 'b-', marker='s', label='topKjoinB')

plt.title('Algorithm Performance Comparison', fontsize=16)
plt.xlabel('K', fontsize=14)
plt.ylabel('Time (sec)', fontsize=14)

plt.legend(fontsize=12)
plt.grid(which='both', linestyle='--', linewidth=0.5)

plt.minorticks_on()

plt.xscale('log')

plt.yscale('log')

plt.ylim(0.001, 100)

plt.xticks(K, labels=[str(k) for k in K], fontsize=12)
plt.yticks([0.001, 0.01, 0.1, 1, 10, 100], fontsize=12)

plt.tick_params(axis='both', which='major', labelsize=12)
plt.tick_params(axis='both', which='minor', labelsize=10)

plt.savefig('detailed_algorithm_performance_comparison.png')

plt.show()
