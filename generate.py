from progress.bar import Bar
import os

bar = Bar('Processing', max=2*(885-10)/5)

for size in range(10, 885, 5):
    os.system('java Maze {0} > maze/maze_{0}_1.txt'.format(size))
    bar.next()
    os.system('java Maze {0} > maze/maze_{0}_2.txt'.format(size))
    bar.next()

bar.finish()
