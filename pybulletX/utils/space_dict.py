# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import gym
import collections

from attrdict import AttrMap


def _override_gym_spaces_dict_constructor():
    """
    Override the existing the constructor of class gym.spaces.Dict.
    The only difference between this and the original __init__ is that space
    in spaces.values() can not only be gym.Space but also any kind of dict-like
    object that conforms to collections.abc.Mapping
    """

    def __init__(self, spaces=None, **spaces_kwargs):
        assert (spaces is None) or (
            not spaces_kwargs
        ), "Use either Dict(spaces=dict(...)) or Dict(foo=x, bar=z)"
        if spaces is None:
            spaces = spaces_kwargs
        if isinstance(spaces, dict) and not isinstance(spaces, collections.OrderedDict):
            spaces = collections.OrderedDict(sorted(list(spaces.items())))
        if isinstance(spaces, list):
            spaces = collections.OrderedDict(spaces)
        self.spaces = spaces
        for key in spaces.keys():
            if isinstance(spaces[key], collections.abc.Mapping):
                spaces[key] = SpaceDict(**spaces[key])
            assert isinstance(
                spaces[key], gym.Space
            ), "Values of the dict should be instances of gym.Space"
        super(gym.spaces.Dict, self).__init__(
            None, None
        )  # None for shape and dtype, since it'll require special handling

    setattr(gym.spaces.Dict, "__init__", __init__)


_override_gym_spaces_dict_constructor()


class SpaceDict(gym.spaces.Dict, collections.abc.Mapping):
    """
    A extension of gym.spaces.Dict that conforms to abc.Mapping
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        return iter(self.spaces)

    def __len__(self):
        return len(self.spaces)

    def __getattr__(self, attr):
        """
        Allow dot (.) access to items in self.spaces
        Note that Python will call __getattr__ whenever you request an attribute
        that hasn't already been defined. If self.spaces hasn't already been
        defined, return an empty dict by default. This is to make sure SpaceDict
        not constructed in the normal way (e.g. by copy.deepcopy) won't get
        "RecursionError: maximum recursion depth".  If attr is in spaces.keys(),
        then return self.spaces[attr]. Otherwise, delegate to super's __getattribute__.
        """
        if attr == "spaces":
            return {}
        if attr in self.spaces.keys():
            return self.spaces[attr]
        return super().__getattribute__(attr)

    def __setitem__(self, key, value):
        self.spaces[key] = value

    def __delitem__(self, attr):
        del self.spaces[attr]

    def __dir__(self):
        return object.__dir__(self) + list(self.spaces.keys())

    def new(self):
        # TODO(poweic): instead of None, use torch.Tensor? (placeholder + strict schema)
        return AttrMap(
            {
                k: v.new() if isinstance(v, collections.abc.Mapping) else None
                for k, v in self.spaces.items()
            }
        )
