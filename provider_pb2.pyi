from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DiffRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DiffResponse(_message.Message):
    __slots__ = ["diffs"]
    DIFFS_FIELD_NUMBER: _ClassVar[int]
    diffs: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, diffs: _Optional[_Iterable[str]] = ...) -> None: ...
