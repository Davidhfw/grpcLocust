import time
from concurrent import futures

import grpc
import sys
sys.path.append("../grpcfiles")
from grpcfiles import sayHello_pb2
from grpcfiles import sayHello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '8080'


class GreeterServicer(sayHello_pb2_grpc.GreeterServicer):
	""" define SayHello function to return what message for client"""

	def SayHello(self, request, ctx):
		max_len = str(len(request.name))
		return sayHello_pb2.HelloReply(message=max_len)


def main():

	# 多线程服务器
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	# 实例化 计算len的类
	servicer = GreeterServicer()
	# 注册本地服务
	sayHello_pb2_grpc.add_GreeterServicer_to_server(servicer, server)
	# 监听端口
	server.add_insecure_port(_HOST + ':' + _PORT)
	# 开始接收请求进行服务
	server.start()
	# 使用ctrl + c 可以退出服务
	try:
		print("running....")
		time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		print("stopping...")
		server.stop(0)


if __name__ == '__main__':
	main()
