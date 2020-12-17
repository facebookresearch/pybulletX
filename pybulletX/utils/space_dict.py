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


def test_space_dict():
    from gym import spaces
    import json

    car = SpaceDict(
        {
            "sensors": SpaceDict(
                {
                    "position": spaces.Box(low=-100, high=100, shape=(3,)),
                    "velocity": spaces.Box(low=-1, high=1, shape=(3,)),
                    "front_cam": spaces.Tuple(
                        (
                            spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                            spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                        )
                    ),
                    "rear_cam": spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                }
            ),
            "ext_controller": spaces.MultiDiscrete((5, 2, 2)),
            "inner_state": {
                "charge": spaces.Discrete(100),
                "system_checks": spaces.MultiBinary(10),
                "job_status": SpaceDict(
                    {
                        "task": spaces.Discrete(5),
                        "progress": spaces.Box(low=0, high=100, shape=()),
                    }
                ),
            },
        }
    )

    print(car)
    print(car.sensors)
    print(car.sensors.position)
    print(car.sensors.velocity)
    print(car.sensors.front_cam)
    print(car.sensors.front_cam[0])
    print(car.sensors.front_cam[1])
    print(car.sensors.rear_cam)
    print(car.inner_state)
    print(car.inner_state.charge)
    print(car.inner_state.system_checks)
    print(car.inner_state.job_status)
    print(car.inner_state.job_status.task)
    print(car.inner_state.job_status.progress)

    print(json.dumps(car.new(), indent=2))


if __name__ == "__main__":
    test_space_dict()
