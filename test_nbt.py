import pytest
import nbtlib
from nbtlib.tag import IntArray, Compound, String

from CreateSG import (
    calculate_relative_pos,
    ArmNBT,
    ConveyorNBT,
    generate_connected_conveyors,
)


def test_calculate_relative_pos():
    assert calculate_relative_pos([5, 5, 5], [1, 2, 3]) == [4, 3, 2]


def test_arm_add_interaction_point():
    arm = ArmNBT(origin=[1, 1, 1])
    arm.add_interaction_point('create:depot', 'TAKE', [3, 2, 0])
    ip = arm.nbt['']['blocks'][0]['nbt']['InteractionPoints'][0]

    assert isinstance(ip, Compound)
    assert ip['Type'] == String('create:depot')
    assert ip['Mode'] == String('TAKE')
    assert list(ip['Pos']) == [2, 1, -1]


def test_arm_add_interaction_point_invalid_mode():
    arm = ArmNBT()
    with pytest.raises(ValueError):
        arm.add_interaction_point('create:depot', 'INVALID', [0, 0, 0])


def test_conveyor_add_connection_single():
    conveyor = ConveyorNBT(origin=[1, 0, 0])
    conveyor.add_connection([1, 2, 3])
    conn = conveyor.nbt['']['blocks'][0]['nbt']['Connections'][0]
    assert isinstance(conn, IntArray)
    assert list(conn) == [0, 2, 3]


def test_conveyor_add_connection_multiple():
    conveyor = ConveyorNBT(origin=[1, 0, 0])
    conveyor.add_connection([[1, 0, 0], [0, 2, 0]])
    conns = conveyor.nbt['']['blocks'][0]['nbt']['Connections']
    assert len(conns) == 2
    assert list(conns[0]) == [0, 0, 0]
    assert list(conns[1]) == [-1, 2, 0]


def test_generate_connected_conveyors(tmp_path):

    # Single coordinate
    filename = tmp_path / "conv.nbt"
    generate_connected_conveyors([10, 0, 0], base_filename=str(filename))


    main_file = tmp_path / "conv_main.nbt"
    inv_file = tmp_path / "conv_1.nbt"
    assert main_file.exists()
    assert inv_file.exists()


    main_nbt = nbtlib.load(str(main_file))
    main_conn = main_nbt[""]["blocks"][0]["nbt"]["Connections"]
    assert len(main_conn) == 1
    assert list(main_conn[0]) == [10, 0, 0]

    inv_nbt = nbtlib.load(str(inv_file))
    inv_conn = inv_nbt[""]["blocks"][0]["nbt"]["Connections"]
    assert len(inv_conn) == 1
    assert list(inv_conn[0]) == [-10, 0, 0]

    # Multiple coordinates origin 50 0 0
    filename2 = tmp_path / "conv2.nbt"
    generate_connected_conveyors([[100, 0, 0], [-100, 0, 0]], base_filename=str(filename2), origin=[50, 0, 0])

    main_file2 = tmp_path / "conv2_main.nbt"
    inv_file1 = tmp_path / "conv2_1.nbt"
    inv_file2 = tmp_path / "conv2_2.nbt"

    assert main_file2.exists()
    assert inv_file1.exists()
    assert inv_file2.exists()

    main2_nbt = nbtlib.load(str(main_file2))
    conns = main2_nbt[""]["blocks"][0]["nbt"]["Connections"]
    assert len(conns) == 2
    assert list(conns[0]) == [50, 0, 0]
    assert list(conns[1]) == [-150, 0, 0]

    inv1_nbt = nbtlib.load(str(inv_file1))
    inv2_nbt = nbtlib.load(str(inv_file2))

    conn1 = inv1_nbt[""]["blocks"][0]["nbt"]["Connections"][0]
    conn2 = inv2_nbt[""]["blocks"][0]["nbt"]["Connections"][0]

    assert list(conn1) == [-50, 0, 0]
    assert list(conn2) == [150, 0, 0]
