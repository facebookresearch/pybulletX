# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import io
from abc import ABCMeta
import collections

from attrdict import AttrMap

from .helper import dump
from .utils.space_dict import SpaceDict


def _remove_empty_dict_leaf(dict_):
    return {
        k: v
        for k, v in dict_.items()
        if not isinstance(v, collections.abc.Mapping) or len(v) > 0
    }


class IRobot(metaclass=ABCMeta):
    """
    Default implementations for state_space/action_space/get_states/set_actions/reset
    """

    @property
    def state_space(self):
        return self.children_state_space

    @property
    def action_space(self):
        return self.children_action_space

    def get_states(self):
        return self.get_children_states()

    def set_actions(self, actions):
        self.set_children_actions(actions)

    def reset(self):
        self.reset_children()

    """
    Recursive implementations for state_space/action_space/get_states/set_actions/reset
    """
    # TODO(poweic): create an iterator class for children() so that we can write
    # self.children().get_states() instead of self.get_children_states()
    @property
    def children_state_space(self):
        return SpaceDict(
            _remove_empty_dict_leaf(
                {k: v.state_space for k, v in self.children().items()}
            )
        )

    @property
    def children_action_space(self):
        return SpaceDict(
            _remove_empty_dict_leaf(
                {k: v.action_space for k, v in self.children().items()}
            )
        )

    def get_children_states(self):
        return AttrMap(
            _remove_empty_dict_leaf(
                {k: v.get_states() for k, v in self.children().items()}
            )
        )

    def set_children_actions(self, actions):
        children = self.children()
        for k, v in actions.items():
            if k not in children:
                continue
            children[k].set_actions(v)

    def reset_children(self):
        for child in self.children().values():
            child.reset()

    def children(self):
        """Get all the children that's also instance of IRobot"""
        return {k: v for k, v in self.__dict__.items() if isinstance(v, IRobot)}

    def __repr__(self):
        output = io.StringIO()
        print(f"State Space: {dump(self.state_space)}", file=output)
        print(f"Action Space: {dump(self.action_space)}", file=output)
        print(f"Current States: {dump(self.get_states())}", file=output)
        print("", file=output)
        return output.getvalue()


def _check_dict_key_collision(d1, d2):
    return set(d1.keys()).intersection(d2.keys())


# FIXME(poweic): how should I name this? router? routeable? hub? switch? pluggable?
def router(func):
    def upward_wrapper(self):
        childrens_attrs = {}
        for k, v in self.children().items():
            attr = getattr(v, func.__name__)
            if callable(attr):
                childrens_attrs[k] = attr()
            else:
                childrens_attrs[k] = attr
        self_attrs = func(self)

        intersection = set(childrens_attrs.keys()).intersection(self_attrs.keys())
        if intersection:
            raise AttributeError(
                f"Found keys {intersection} in both childrens_attrs and self_attrs"
            )

        attrs = {**childrens_attrs, **self_attrs}
        attrs = _remove_empty_dict_leaf(attrs)

        # TODO(poweic): It's confusing to have both SpaceDict & AttrMap at the same
        # time. Also, return AttrMap in new() method of SpaceDict is weird.
        # Consider creating that's both SpaceDict and AttrMap at the same time.
        if func.__name__ == "get_states":
            attrs = AttrMap(attrs)
        else:
            attrs = SpaceDict(attrs)

        return attrs

    def downward_wrapper(self, attrs):
        children = self.children()
        self_attrs = {k: v for k, v in attrs.items() if k not in children.keys()}
        func(self, self_attrs)

        childrens_attrs = {k: v for k, v in attrs.items() if k in children.keys()}

        for k, v in childrens_attrs.items():
            child = children[k]
            f = getattr(child, func.__name__)
            f(attrs[k])

    if func.__name__ == "set_actions":
        return downward_wrapper
    else:
        return upward_wrapper
