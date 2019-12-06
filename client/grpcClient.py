import sys
sys.path.append('../grpcfiles')
sys.path.append('../common')
import time
import grpc
from locust import events, Locust
from common import config

class GrpcClient(object):
	"""
	定义Grpc协议自己的请求客户端，用于将locust默认支持的http协议客户端替换
	"""

	def __init__(self):
		self.host = config._HOST
		self.port = config._PORT

	def setup_channel_without_cert(self):
		"""
		建立无需证书的连接通道
		:return:
		"""
		try:
			conn = grpc.insecure_channel(self.host + ':' + self.port)
		except grpc.RpcError as e:
			print("Request error: ", e)
		except Exception as e:
			print("Unknown error: ", e)
		else:
			return conn


	def connect_without_cert(self, rpc_api_func, task_name, **kwargs):
		"""
		grpc连接请求实例，不需要认证证书
		:param task_name: 任务名称
		:param rpc_api_func: rpc接口请求函数
		:param kwargs: 请求参数, 这里以可变关键参数，取值可按照字典取值操作
		:return: 响应内容
		"""
		res = ""
		start_time = int(time.time())
		try:
			res = rpc_api_func(conn=self.setup_channel_without_cert(), **kwargs)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="grpc", name='/' + task_name, response_time=total_time,
			                            response_length=0, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="grpc", name='/' + task_name, response_time=total_time,
			                            response_length=0)
		return res
    
    
class GrpcLocust(Locust):
	"""
	This is the abstract Locust class which should be subclassed. It provides an GRPC client
	that can be used to make GRPC requests that will be tracked in Locust's statistics.
	"""

	def __init__(self):
		super().__init__()
		self.client = GrpcClient()
