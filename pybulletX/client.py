# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import functools
import threading

import pybullet as p
import pybulletX as px

log = logging.getLogger(__name__)


class Client:
    def __init__(self, mode: int = None, client_id: int = None):
        # should provide either mode or client_id but not both
        # mode and client_id can't be both None at the same time.
        # This is equiv. to XOR test
        assert (mode is None) != (client_id is None)

        if client_id is None:
            self._initialized_by_us = True
            self._id = px.init(mode=mode)
        else:
            self._initialized_by_us = False
            self._id = client_id

    @property
    def id(self):
        return self._id

    def release(self):
        if not self._initialized_by_us:
            return

        try:
            log.info(f"Physics client {self.id} disconnected.")
            self.disconnect()
        except:
            ...

    def __enter__(self):
        self.prev_client = current_client()
        set_client(self)
        return self

    def __exit__(self, *args, **kwargs):
        set_client(self.prev_client)

    """
    # TODO(poweic): this might not always got called
    def __del__(self):
        self.release()
    """

    def _apply(self, func_name, *args, **kwargs):
        func = getattr(p, func_name)
        return func(*args, **kwargs, physicsClientId=self._id)


# Note(poweic): This is very similar to torch.cuda.current_device,
# torch.cuda.set_device
_tls = threading.local()

# By default, pybullet use client_id = 0 for all API.
_tls.current_client = Client(client_id=0)


def current_client() -> Client:
    return _tls.current_client


def set_client(client: Client):
    _tls.current_client = client


func_names = [
    # Basics
    "disconnect",
    "isConnected",
    "setGravity",
    "loadURDF",
    "loadSDF",
    "loadMJCF",
    "saveState",
    "saveBullet",
    "restoreState",
    "createCollisionShape",
    "createCollisionShapeArray",
    "removeCollisionShape",
    "createVisualShape",
    "createVisualShapeArray",
    "createMultiBody",
    "getMeshData",
    "stepSimulation",
    "setRealTimeSimulation",
    "getBasePositionAndOrientation",
    "resetBasePositionAndOrientation",
    # Controlling a robot
    "getNumJoints",
    "getJointInfo",
    "setJointMotorControl2",
    "setJointMotorControlArray",
    "setJointMotorControlMultiDof",
    "setJointMotorControlMultiDofArray",
    "getJointState",
    "getJointStates",
    "getJointStateMultiDof",
    "getJointStatesMultiDof",
    "resetJointState",
    "resetJointStateMultiDof",
    "resetJointStatesMultiDof",
    "enableJointForceTorqueSensor",
    "getLinkState",
    "getLinkStates",
    "getBaseVelocity",
    "resetBaseVelocity",
    "applyExternalForce",
    "applyExternalTorque",
    "getNumBodies",
    "getBodyInfo",
    "getBodyUniqueId",
    "removeBody",
    # Constraints
    "createConstraint",
    "changeConstraint",
    "removeConstraint",
    "getNumConstraints",
    "getConstraintUniqueId",
    "getConstraintInfo",
    "getConstraintState",
    # Dynamics
    "getDynamicsInfo",
    "changeDynamics",
    # Physics Engine Parameters
    "setTimeStep",
    "setPhysicsEngineParameter",
    "getPhysicsEngineParameters",
    "resetSimulation",
    # Logging
    "startStateLogging",
    "stopStateLogging",
    # Synthetic Camera Rendering
    "getCameraImage",
    "getVisualShapeData",
    "changeVisualShape",
    "loadTexture",
    # Collision Detection
    "getOverlappingObjects",
    "getAABB",
    "getContactPoints",
    "getClosestPoints",
    "rayTest",
    "rayTestBatch",
    "getCollisionShapeData",
    "vhacd",
    "setCollisionFilterGroupMask",
    "setCollisionFilterPair",
    # Inverse Dynamics & Kinematics
    "calculateInverseDynamics",
    "calculateJacobian",
    "calculateMassMatrix",
    "calculateInverseKinematics",
    "calculateInverseKinematics2",
    # Virtual Reality
    "getVREvents",
    "setVRCameraState",
    # Debug/GUI
    "addUserDebugLine",
    "addUserDebugText",
    "addUserDebugParameter",
    "removeAllUserParameters",
    "removeUserDebugItem",
    "setDebugObjectColor",
    "configureDebugVisualizer",
    "resetDebugVisualizerCamera",
    "getDebugVisualizerCamera",
    "getKeyboardEvents",
    "getMouseEvents",
    # Plugins
    "loadPlugin",
    "executePluginCommand",
    "unloadPlugin",
]

for func_name in func_names:
    getattr(p, func_name)
    partial = functools.partialmethod(Client._apply, func_name)
    setattr(Client, func_name, partial)

Client.getContactPoints = px.contact_point.decorator(Client.getContactPoints)
