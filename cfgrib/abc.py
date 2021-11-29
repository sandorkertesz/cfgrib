"""Abstract Base Classes for GRIB fields and fieldsets"""
import abc
import typing as T

FieldIdTypeVar = T.TypeVar("FieldIdTypeVar", contravariant=True)
FieldTypeVar = T.TypeVar("FieldTypeVar", bound="Field", covariant=True)

Field = T.Mapping[str, T.Any]
MutableField = T.MutableMapping[str, T.Any]
MappingFieldset = T.Mapping[FieldIdTypeVar, FieldTypeVar]
SequenceFieldset = T.Sequence[FieldTypeVar]


class Getter(T.Protocol[FieldIdTypeVar, FieldTypeVar]):
    def __getitem__(self, item: FieldIdTypeVar) -> FieldTypeVar:
        raise NotImplementedError


class Index(T.Mapping[str, T.List[T.Any]], T.Generic[FieldIdTypeVar, FieldTypeVar]):
    fieldset: Getter[FieldIdTypeVar, FieldTypeVar]
    index_keys: T.List[str]
    filter_by_keys: T.Dict[str, T.Any] = {}

    @abc.abstractmethod
    def subindex(
        self, filter_by_keys: T.Mapping[str, T.Any] = {}, **query: T.Any
    ) -> "Index[FieldIdTypeVar, FieldTypeVar]":
        pass

    @abc.abstractmethod
    def getone(self, item: str) -> T.Any:
        pass

    @abc.abstractmethod
    def first(self) -> FieldTypeVar:
        pass

    @abc.abstractmethod
    def source(self) -> str:
        pass

    @abc.abstractmethod
    def iter_index(self) -> T.Iterator[T.Tuple[T.Tuple[T.Any, ...], T.List[FieldIdTypeVar]]]:
        pass
