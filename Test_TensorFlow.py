from __future__ import division, print_function, unicode_literals

import numpy as np
import os
import tensorflow as tf

# reset_graph()

x = tf.Variable(3, name="x")
y = tf.Variable(4, name="y")
f = x*x*y + y + 2

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

sess = tf.Session()
sess.run(x.initializer)
sess.run(y.initializer)
result = sess.run(f)
print(result)

sess.close()

with tf.Session() as sess:
	x.initializer.run()
	y.initializer.run()
	result = f.eval()


init = tf.global_variables_initializer()

with tf.Session() as sess:
	init.run()
	result = f.eval()


init = tf.global_variables_initializer()

sess = tf.InteractiveSession()
init.run()
result = f.eval()
print(result)

sess.close()



if __name__ == "__main__":
	print ("\nOK!\n")
	print ("\nDone!\n")