# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging as _logging
import pybullet as _pybullet
import numpy as _numpy

from .joint_info import JointInfo
from .joint_state import JointState
from .link_state import LinkState
from .dynamics_info import DynamicsInfo


_log = _logging.getLogger(__name__)


def _to_struct_of_array(array_of_struct):
    """
    utility function that convert array of struct (AoS) to struct of array (SoA),
    which is more suitable for ML application down the road (ex: PyTorch).
    """
    if not array_of_struct:
        return {}
    keys = array_of_struct[0].__dict__.keys()
    return {
        k: _numpy.array([getattr(struct, k) for struct in array_of_struct])
        for k in keys
    }


# store the original pybullet global functions here
class _orig_pybullet:
    getJointState = _pybullet.getJointState
    getJointStates = _pybullet.getJointStates

    getLinkState = _pybullet.getLinkState
    getLinkStates = _pybullet.getLinkStates

    # Unlike getJointState/getJointStates and getLinkState/getLinkStates,
    # there is only one function for getting joint information in pybullet
    # , which is getJointInfo
    getJointInfo = _pybullet.getJointInfo

    getDynamicsInfo = _pybullet.getDynamicsInfo


def _getJointInfo(*args, **kwargs):
    joint_info_tuple = _orig_pybullet.getJointInfo(*args, **kwargs)
    joint_info = JointInfo(*joint_info_tuple)
    return joint_info


def _getJointInfos(bodyUniqueId, jointIndices, **kwargs):
    joint_info_tuples = [
        _orig_pybullet.getJointInfo(bodyUniqueId, joint_index, **kwargs)
        for joint_index in jointIndices
    ]

    if joint_info_tuples:
        joint_infos = list(map(_numpy.array, zip(*joint_info_tuples)))
        joint_infos = JointInfo(*joint_infos)
        joint_infos._plural = True
        joint_infos._data = joint_info_tuples
        return joint_infos
    else:
        return None


def _getJointState(*args, **kwargs):
    joint_state_tuple = _orig_pybullet.getJointState(*args, **kwargs)
    joint_state = JointState(*joint_state_tuple)
    return joint_state


def _getJointStates(*args, **kwargs):
    joint_state_tuples = _orig_pybullet.getJointStates(*args, **kwargs)
    if not joint_state_tuples:
        return None

    # tranpose tuple of tuples using zip & map
    joint_states = list(map(_numpy.array, zip(*joint_state_tuples)))
    joint_states = JointState(*joint_states)
    joint_states._plural = True
    joint_states._data = joint_state_tuples
    return joint_states


def _getLinkState(*args, **kwargs):
    link_state_tuple = _orig_pybullet.getLinkState(*args, **kwargs)
    link_state = LinkState(*link_state_tuple)
    return link_state


def _getLinkStates(*args, **kwargs):
    link_state_tuples = _orig_pybullet.getLinkStates(*args, **kwargs)
    if not link_state_tuples:
        return None

    link_states = list(map(_numpy.array, zip(*link_state_tuples)))
    link_states = LinkState(*link_states)
    link_states._plural = True
    link_states._data = link_state_tuples
    return link_states


def _getDynamicsInfo(bodyUniqueId, linkIndex, **kwargs):
    dynamics_info_tuple = _orig_pybullet.getDynamicsInfo(
        bodyUniqueId, linkIndex, **kwargs
    )
    dynamics_info = DynamicsInfo(*dynamics_info_tuple)
    return dynamics_info


def _getDynamicsInfos(bodyUniqueId, linkIndices, **kwargs):
    dynamics_info_tuples = [
        _orig_pybullet.getDynamicsInfo(bodyUniqueId, link_index, **kwargs)
        for link_index in linkIndices
    ]

    if dynamics_info_tuples:
        dynamics_infos = list(map(_numpy.array, zip(*dynamics_info_tuples)))
        dynamics_infos = DynamicsInfo(*dynamics_infos)
        dynamics_infos._plural = True
        dynamics_infos._data = dynamics_info_tuples
        return dynamics_infos
    else:
        return None


def _setParameters(cfg, physicsClientId=None):
    r"""
    A helper function that sets multiple parameters of pybullet from a dict-like
    object.

    Example::
        >>> pybullet.setParameters({
              "gravity": {
                "gravX": 0,
                "gravY": 0,
                "gravZ": -9.81,
              },
              "timeStep": 0.001,
              "physicsEngineParameter": {
                "numSolverIterations": 2000,
                "solverResidualThreshold": 1e-30,
                "reportSolverAnalytics": True,
              }
            })
    """
    for key, value in cfg.items():
        setter_method_name = "set{}".format(key[0].upper() + key[1:])
        setter = getattr(_pybullet, setter_method_name)

        args = []
        kwargs = {}

        # if value is a dict-like, copy it to kwargs. Otherwise, treat value as args
        try:
            # FIXME(poweic): should use isinstance(value, collections.abc.Mapping)
            # but some of the useful package (ex: OmegaConf) doesn't inherits from
            # collections.abc.Mapping. Use try except instead.
            kwargs = dict(**value)
        except TypeError:
            args.append(value)

        if physicsClientId is not None:
            kwargs["physicsClientId"] = physicsClientId

        param_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        _log.info(f"Calling pybullet.{setter_method_name}({param_str})")
        setter(*args, **kwargs)


def _replace_original_methods():
    _pybullet.getJointInfo = _getJointInfo
    _pybullet.getJointInfos = _getJointInfos

    _pybullet.getJointState = _getJointState
    _pybullet.getJointStates = _getJointStates

    _pybullet.getLinkState = _getLinkState
    _pybullet.getLinkStates = _getLinkStates

    _pybullet.getDynamicsInfo = _getDynamicsInfo
    _pybullet.getDynamicsInfos = _getDynamicsInfos

    assert not hasattr(_pybullet, "setParameters")
    _pybullet.setParameters = _setParameters


_exported_dunders = {
    "__version__",
}

__all__ = [s for s in dir() if s in _exported_dunders or not s.startswith("_")]
