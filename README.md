When running a server with `grpcio>=1.58.0` and calling a by-design unimplemented method on the service, a traceback is emitted to stderr.

This was introduced in 1.58.0 with https://github.com/grpc/grpc/pull/33442

When running the server on prior versions (e.g. `grpcio==1.57.0`), no traceback is emitted when calling the unimplemented method.

This is problematic because our client redirects the output of the server's stdout and stderr, and displays it to users. Previously, with 1.57.0 and earlier, nothing would be displayed to users. But with 1.58.0 or greater, the traceback is displayed to users.

This is preventing us from supporting Python 3.12, which requires `grpcio` 1.59.0.

## About this repro

The server is implemented in `server.py`. There is a `MyResourceProviderServicer` that has an unimplemented `DiffConfig` method.

The client is implemented in `client.py`. Running the client will start the server and redirect it's stdout and stderr. The client calls `DiffConfig`, which is unimplemented (which the client handles gracefully), and then kills th server and exits.

When running with grpcio 1.57.0 and earlier, running `python client.py` emits nothing to stdout or stderr.

When running with grpcio 1.58.0 and greater, running `python client.py` emits the traceback from the server, which is undesirable for our usage.

## Repro steps

1. Clone this repository.


2. Install dependencies in a virtual environment with the following commands on macOS or Linux:

```sh
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

3. Run the client (which automatically starts the server and redirects it's stdout and stderr):

```
python client.py
```

Notice, nothing is outputted to stdout or stderr.

4. Upgrade to grpcio from 1.57.0 to 1.58.0:

```
pip install grpcio==1.58.0
```

5. Run the client again:

```
python client.py
```

Notice the following is emitted to stderr:

```
Traceback (most recent call last):
  File "/Users/justin/go/src/github.com/justinvp/grpc-python-repro/venv/lib/python3.10/site-packages/grpc/_server.py", line 552, in _call_behavior
    response_or_iterator = behavior(argument, context)
  File "/Users/justin/go/src/github.com/justinvp/grpc-python-repro/provider_pb2_grpc.py", line 31, in DiffConfig
    raise NotImplementedError('Method not implemented!')
NotImplementedError: Method not implemented!
```

## Expected

No output to stderr or stdout when calling an unimplemented.

## Actual

A traceback is emitted to stderr.
