# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

import pybullet as p
import pybulletX as px


@pytest.mark.xfail
def test_client_destructor():
    r"""
    Create a few clients, store them in the list. Use p.isConnected
    to check connectivity after deleting the list.
    """
    clients = [px.Client(mode=p.DIRECT) for i in range(5)]
    client_ids = [client.id for client in clients]

    for cid in client_ids:
        assert p.isConnected(cid)

    del clients

    for cid in client_ids:
        assert not p.isConnected(cid)
