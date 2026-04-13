import time
import random
import multiprocessing
from collections import Counter

def process_chunk(chunk):
    return [x for x in chunk if x > 0]

def main():
    # Умова варіанту 5: 100 000 елементів
    size = 100000
    data = [random.randint(-500, 500) for _ in range(size)]
    
    print(f"Аналіз для масиву розміром {size} елементів:\n")
    start_seq = time.perf_counter()
    
    pos_seq = [x for x in data if x > 0]
    pos_seq.sort()
    grouped_seq = Counter(pos_seq)
    
    time_seq = time.perf_counter() - start_seq

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    
    start_par = time.perf_counter()
    
    chunk_size = size // num_cores
    chunks = [data[i:i + chunk_size] for i in range(0, size, chunk_size)]
    
    results = pool.map(process_chunk, chunks)
    
    pos_par = [item for sublist in results for item in sublist]
    pos_par.sort()
    grouped_par = Counter(pos_par)
    
    time_par = time.perf_counter() - start_par
    pool.close() 
    pool.join()


    print(f"{'Метод':<15} | {'Час виконання (сек)':<20}")
    print("-" * 40)
    print(f"{'Послідовно':<15} | {time_seq:.6f}")
    print(f"{'Паралельно':<15} | {time_par:.6f}")
    
    if time_par < time_seq:
        print(f"\nПрискорення: {time_seq / time_par:.2f}x")
    

    print("\nРезультат (перші 5 груп):")
    for val, count in list(grouped_par.items())[:5]:
        print(f"Число {val}: {count} разів")

if __name__ == "__main__":
    main()