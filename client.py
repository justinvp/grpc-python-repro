import subprocess
import sys
import time
from typing import Optional, cast

import grpc
import provider_pb2
import provider_pb2_grpc


def run():
    p = subprocess.Popen(["python", "server.py"], stdout=sys.stdout, stderr=sys.stderr)

    time.sleep(2) # wait a couple seconds for the server to start

    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = provider_pb2_grpc.ResourceProviderStub(channel)

            try:
                # Call DiffConfig. It's OK if it's unimplemented.
                stub.DiffConfig(provider_pb2.DiffRequest(id="test"))
            except grpc.RpcError as error:
                future = cast(grpc.Future, error)
                ex: Optional[grpc.Call] = future.exception()
                if ex is None or ex.code() != grpc.StatusCode.UNIMPLEMENTED:
                    raise error
    except Exception as e:
        print(e)
    finally:
        p.kill()


if __name__ == "__main__":
    run()
