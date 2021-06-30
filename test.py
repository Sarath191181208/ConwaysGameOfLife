import threading
import time 

def threadFunc(num):
	for i in range(5):
		print(f'HEllo {num} from new Thread')
		time.sleep(1)

def main():
	print("oof")
	th = threading.Thread(target=threadFunc(5))

	th.start()

	for i in range(20):
		print('main')
		time.sleep(2)

	th.join()

if __name__ == '__main__':
	main()
