
import sys
sys.path.append("../grpcfiles")
from grpcfiles import sayHello_pb2
from grpcfiles import sayHello_pb2_grpc


class RpcApiTestColl(object):
	"""
	define rpc api test function
	"""
	def __init__(self):
		pass

	# 定义自己的rpc api的请求与返回
	@staticmethod
	def sayhello_rpc_api_test(conn, **kwargs):
		"""
		发送请求并获得响应，不需要证书
		:param conn: 非证书通道连接
		:param kwargs: 请求方法所需参数
		:return: 响应内容
		"""
		try:
			client = sayHello_pb2_grpc.GreeterStub(channel=conn)
			req_args_init = sayHello_pb2.HelloRequest(**kwargs)
			res = client.SayHello(req_args_init)
		except Exception as e:
			raise e
		else:
			return res
