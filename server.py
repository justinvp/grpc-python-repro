from concurrent import futures

import grpc
import provider_pb2_grpc


class MyResourceProviderServicer(provider_pb2_grpc.ResourceProviderServicer):
    def __init__(self):
        pass

    def DiffConfig(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    provider_pb2_grpc.add_ResourceProviderServicer_to_server(
        MyResourceProviderServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
