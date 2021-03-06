import gym,time,threading
import tensorflow as tf

ENV_NAME = 'Breakout-v0'
THREADS = 2

# env = gym.make(ENV_NAME)
# env.reset()

# print env.observation_space
# print env.action_space.n
# print env.observation_space.high
# print env.action_space.high

# for i in range(1000):
# 	env.render()
# 	obs,reward,done,_ = env.step(env.action_space.sample())
# 	# time.sleep(0.02)
# 	if(i%1000==0):
# 		print env.action_space.sample()

# 	if done:
# 		break

#dans ce program le brain est l'inteligence et il agira sur plusieurs agents en meme temps
class Brain():
	"""le brain est l'inteligence artificielle."""
	def __init__(self):
		epi_transitions = []
		self.sess = tf.Session()

		ModelPack = self.Build_Model()


		self.sess.run(tf.global_variables_initializer())

	def Build_Model():
		# with tf.variable_scope("value"):
		l_o = tf.placeholder(tf.float32,[None,NUM_OBS])

		# 	with tf.name_scope("FCLayer"):
		wv1 = tf.Variable(tf.random_normal([NUM_OBS,16]))
		bv1 = tf.Variable(tf.zeros([16]))
		l_hidden = tf.nn.relu(tf.matmul(l_o,wv1) + bv1)

		wv2 = tf.Variable(tf.random_normal([16,1]))
		bv2 = tf.Variable(tf.zeros([1]))
		v = tf.matmul(l_hidden,wv2) + bv2


		wp1 = tf.Variable(tf.random_normal([NUM_OBS,16]))
		bp1 = tf.Variable(tf.zeros([16]))
		l_hidden = tf.nn.relu(tf.matmul(l_o,wp1) + bp1)

		wp2 = tf.Variable(tf.random_normal([16,NUM_ACTIONS]))
		bp2 = tf.Variable(tf.zeros([NUM_ACTIONS]))
		p = tf.nn.softmax(tf.matmul(l_hidden,wp2) + bp2)

		return v,p,l_o

	def Build_Optimizer(ModelPack):
		v,p,l_o = ModelPack


	def Predict(o):
		p,v = self.sess.run([policy,value],{l_o : o})
		return p,v

class Agent():
	"""l'Agent est l'equivalent d'une telecommande pour le Brain, il en gere plusieurs en meme temps"""
	def __init__(self):
		
		


class Environement(threading.Thread):
	stop_signal = False

	def __init__(self,max_steps,render=False):
		threading.Thread.__init__(self)

		self.render = render
		self.env = gym.make(ENV_NAME)
		self.agent = Agent()
		self.max_steps = max_steps

	def runEpisode(self):
		o = self.env.reset()

		R = 0
		for step in range(self.max_steps):

			if self.render : self.env.render()

			a = self.env.action_space.sample()

			o_ , r ,done, _ = self.env.step(a)

			if done :
				break

			o = o_
			R+=r
		

		return R

	def run(self):
		while not self.stop_signal:
			self.runEpisode()

	def stop(self):
		self.stop_signal = True

##MAIN

envs = [Environement(1000) for i in range(THREADS)]
envs[0].render = True

NUM_OBS = envs[0].env.observation_space.shape[0]
NUM_ACTIONS = envs[0].env.action_space.n


print "Before"

for e in envs:
	e.start()

time.sleep(10)

for e in envs:
	e.stop()
for e in envs:
	e.join()

print "After"
