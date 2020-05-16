from progress.bar import Bar
import subprocess
import json
import math

algorithms = {
	'Sasha1': {
		'time': {},
		'path': {},
		'times': 2,
		'timeout': lambda x: 1,
		'break': True,
		'src': 'Sasha1.txt'
	},
	'Sasha2': {
		'time': {},
		'path': {},
		'times': 6,
		'timeout': lambda x: math.exp(math.log(30) / 175 * x),  # from 1s to 30s as x from 1 to 175
		'break': False,
		'src': 'Sasha2.txt'
	},
	'Misha1': {
		'time': {},
		'path': {},
		'times': 6,
		'timeout': lambda x: 1,
		'break': False,
		'src': 'Misha1.txt'
	},
}

bad_attempts = 0
total_attempts = 0

for a in algorithms:
	times = algorithms[a]['times']
	timeout = algorithms[a]['timeout']
	break_policy = algorithms[a]['break']
	bar = Bar('Bench ' + a, max=175 * 2 * times)  # 175

	for size in range(885, 525, 5):  # 885
		time_average = 0
		path_size_average = 0
		attempts = 0
		mazes = ['maze/maze_%d_1.txt' % size, 'maze/maze_%d_2.txt' % size]

		for maze in mazes:
			try:
				for t in range(0, times):
					total_attempts += 1
					try:
						time = subprocess.check_output(['java', a, str(size), maze], timeout=timeout((size - 10) / 5))
						out = time.decode("utf-8").split("\n")
						time_average += float(out[0])
						path_size_average += int(out[1])
						bar.next()
						attempts += 1
					except subprocess.TimeoutExpired:
						bad_attempts += 1
						if break_policy:
							raise ValueError('')
						else:
							bar.next()
							continue

			except ValueError:
				bar.next(times)
				continue

		if attempts > 0:
			algorithms[a]['time'][size] = time_average / attempts
			algorithms[a]['path'][size] = path_size_average / attempts

	bar.finish()

	with open(algorithms[a]['src'], "w") as file:
		del algorithms[a]['timeout']  # fix for: Object of type function is not JSON serializable
		file.write(json.dumps(algorithms[a]))

print("ratio = %d/%d = %f" % (bad_attempts, total_attempts, bad_attempts / total_attempts))
