from gevent._semaphore import Semaphore
from locust import TaskSet, task, between, events
import sys
sys.path.append('../client')
sys.path.append('../rpcapitest')
sys.path.append('../common')
from client.grpcClient import GrpcLocust
from rpcapitest.rpcapitestdemo import RpcApiTestColl
from common.log_config import LoggerConfig
LOG_FILE_NAME = '../common/log.yaml'

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()




def on_hatch_complete(**kwargs):
	# 创建钩子方法
	all_locusts_spawned.release()


# 挂载到locust钩子函数（所有的Locust实例产生完成时触发）
events.hatch_complete += on_hatch_complete


class GrpcTask(TaskSet):
	"""
	Stress Testing
	"""
	def on_start(self):

		""" on_start is called when a Locust start before any task is scheduled """
		# 限制在所有用户准备完成前处于等待状态
		all_locusts_spawned.wait()

	def on_stop(self):
		""" on_stop is called when the TaskSet is stopping """
		pass

	@task(10)
	def sayhello(self):
		name = 'Hello, how are you!'
		task_name = sys._getframe().f_code.co_name
		log_conf = LoggerConfig(LOG_FILE_NAME)
		res = self.client.connect_without_cert(task_name=task_name,
		                                       rpc_api_func=RpcApiTestColl.sayhello_rpc_api_test,
		                                       name=name)


class WebSiteUser(GrpcLocust):
	task_set = GrpcTask
	wait_time = between(1, 10)


if __name__ == '__main__':
	import random
	import string
	import os
	rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	os.system('locust -f grpcTask.py --csv="../csvdata/example_{rand_str}" --no-web -c 10 -r 4  --run-time 10s'.format(rand_str=rand_str))
