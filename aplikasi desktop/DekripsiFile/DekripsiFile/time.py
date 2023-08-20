import time

def stopwatch():
    start_time = time.time()
    input("Tekan 'Enter' untuk menghentikan stopwatch.")
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time = round(elapsed_time, 2)
    print(f"Waktu yang telah berlalu: {elapsed_time} detik")

stopwatch()
