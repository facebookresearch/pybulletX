# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import collections


class MappingMixin(collections.abc.Mapping):
    def __new__(cls, *args):
        inst = super().__new__(cls)
        inst.__init__(*args)
        inst._data = args
        return inst

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            value = self._data[key]
            if self._plural:
                return self.__class__(*value)
            else:
                return value

        return self.__dict__[key]

    def keys(self):
        for k in self.__dict__.keys():
            if not k.startswith("_"):
                yield k

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def __iter__(self):
        if self._plural:
            return (self[i] for i in range(len(self)))
        else:
            return self.keys()

    def __len__(self):
        # return len(self.__dict__)
        return len(self._data)
