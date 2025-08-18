import nbtlib
from nbtlib.tag import Compound, List, Int, IntArray, Float, String, Byte
from typing import List as ListType, Tuple, Optional, Union

Coord = Union[ListType[int], Tuple[int, int, int]]


def create_arm_template() -> nbtlib.File:
    """
    Creates a template NBT structure for a Create mod Mechanical Arm.

    This function generates a default nbtlib.File object with the necessary
    tags and structure for a single Mechanical Arm block, ready to be
    customized.

    Parameters
    ----------
    None

    Returns
    -------
    nbtlib.File
        An nbtlib.File object representing a default Mechanical Arm.
    """
    return nbtlib.File(
        {
            '': Compound(
                {
                    'size': List[Int]([Int(1), Int(1), Int(1)]),
                    'blocks': List[Compound](
                        [
                            Compound(
                                {
                                    'state': Int(0),
                                    'pos': List[Int]([Int(0), Int(0), Int(0)]),
                                    'nbt': Compound(
                                        {
                                            'NeedsSpeedUpdate': Byte(1),
                                            'Phase': String('SEARCH_INPUTS'),
                                            'InteractionPoints': List[Compound]([]),
                                            'id': String('create:mechanical_arm'),
                                            'Speed': Float(0.0),
                                            'Powered': Byte(0),
                                            'Goggles': Byte(0),
                                            'ScrollValue': Int(0),
                                            'MovementProgress': Float(0.0),
                                            'TargetPointIndex': Int(0),
                                            'HeldItem': Compound({}),
                                        }
                                    ),
                                }
                            )
                        ]
                    ),
                    'palette': List[Compound](
                        [
                            Compound(
                                {
                                    'Name': String('create:mechanical_arm'),
                                    'Properties': Compound({'ceiling': String('false')}),
                                }
                            )
                        ]
                    ),
                    'entities': List([]),
                    'DataVersion': Int(3955),
                }
            )
        }
    )


def create_conveyor_template() -> nbtlib.File:
    """
    Creates a template NBT structure for a Create mod Chain Conveyor.

    This function generates a default nbtlib.File object with the necessary
    tags and structure for a single Chain Conveyor block, ready to be
    customized.

    Parameters
    ----------
    None

    Returns
    -------
    nbtlib.File
        An nbtlib.File object representing a default Chain Conveyor.
    """
    return nbtlib.File(
        {
            '': Compound(
                {
                    'size': List[Int]([Int(1), Int(1), Int(1)]),
                    'blocks': List[Compound](
                        [
                            Compound(
                                {
                                    'state': Int(0),
                                    'pos': List[Int]([Int(0), Int(0), Int(0)]),
                                    'nbt': Compound(
                                        {
                                            'LoopingPackages': List([]),
                                            'NeedsSpeedUpdate': Byte(1),
                                            'id': String('create:chain_conveyor'),
                                            'Speed': Float(0.0),
                                            'TravellingPackages': List([]),
                                            'Connections': List[IntArray]([]),
                                        }
                                    ),
                                }
                            )
                        ]
                    ),
                    'palette': List[Compound](
                        [Compound({'Name': String('create:chain_conveyor')})]
                    ),
                    'entities': List([]),
                    'DataVersion': Int(3955),
                }
            )
        }
    )


def calculate_relative_pos(pos: Coord, origin: Coord) -> ListType[int]:
    """
    Calculate the relative position of a point with respect to an origin.

    Parameters
    ----------
    pos : Union[ListType[int], Tuple[int, int, int]]
        The absolute position [x, y, z] of the point.
    origin : Union[ListType[int], Tuple[int, int, int]]
        The absolute position [x, y, z] of the origin.

    Returns
    -------
    ListType[int]
        A list containing the relative coordinates [x, y, z].
    """
    return [p - o for p, o in zip(pos, origin)]


class BaseNBT:
    """
    A base class for creating and manipulating NBT structures for Create mod items.

    Attributes
    ----------
    origin : ListType[int]
        The origin coordinates [x, y, z] used for calculating relative positions.
    nbt : nbtlib.File
        The nbtlib.File object holding the NBT data.
    """

    def __init__(self, origin: Optional[Coord] = None) -> None:
        """
        Initializes the BaseNBT object.

        Parameters
        ----------
        origin : Optional[Union[ListType[int], Tuple[int, int, int]]], optional
            The origin [x, y, z] for position calculations. Defaults to [0, 0, 0].

        Returns
        -------
        None
        """
        self.origin: ListType[int] = list(origin) if origin else [0, 0, 0]
        self.nbt: nbtlib.File = self._create_template()

    def _create_template(self) -> nbtlib.File:
        """
        Creates the template NBT file structure.

        This method is intended to be overridden by subclasses to provide a specific
        NBT template for a particular block or item.

        Parameters
        ----------
        None

        Returns
        -------
        nbtlib.File
            An nbtlib.File object representing the template.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    def save(self, filename: str, gzipped: bool = True) -> None:
        """
        Saves the NBT data to a file.

        Parameters
        ----------
        filename : str
            The path and name of the file to save the NBT data to.
        gzipped : bool, optional
            Whether to use GZip compression for the output file. Defaults to True.

        Returns
        -------
        None
        """
        self.nbt.save(filename, gzipped=gzipped)


class ArmNBT(BaseNBT):
    """
    Represents a Create mod Mechanical Arm NBT structure, inheriting from BaseNBT.

    This class provides methods to customize a Mechanical Arm's NBT data,
    such as adding interaction points.
    """

    def _create_template(self) -> nbtlib.File:
        """
        Creates the specific NBT template for a Mechanical Arm.

        Parameters
        ----------
        None

        Returns
        -------
        nbtlib.File
            An nbtlib.File object representing a default Mechanical Arm.
        """
        return create_arm_template()

    def add_interaction_point(self, type_str: str, mode: str, pos: Coord) -> None:
        """
        Adds an interaction point to the Mechanical Arm's NBT data.

        Parameters
        ----------
        type_str : str
            The type of interaction point (e.g., 'create:depot').
        mode : str
            The interaction mode, must be either 'TAKE' or 'DEPOSIT'.
        pos : Union[ListType[int], Tuple[int, int, int]]
            The absolute world coordinates [x, y, z] of the interaction point.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the mode is not 'TAKE' or 'DEPOSIT'.
        """
        if mode not in ['TAKE', 'DEPOSIT']:
            raise ValueError("Mode must be 'TAKE' or 'DEPOSIT'")
        relative_pos = calculate_relative_pos(pos, self.origin)
        interaction_point = Compound(
            {
                'Type': String(type_str),
                'Mode': String(mode),
                'Pos': IntArray([Int(x) for x in relative_pos]),
            }
        )
        self.nbt['']['blocks'][0]['nbt']['InteractionPoints'].append(interaction_point)


class ConveyorNBT(BaseNBT):
    """
    Represents a Create mod Chain Conveyor NBT structure, inheriting from BaseNBT.

    This class provides methods to customize a Chain Conveyor's NBT data,
    such as adding connections to other conveyors.
    """

    def _create_template(self) -> nbtlib.File:
        """
        Creates the specific NBT template for a Chain Conveyor.

        Parameters
        ----------
        None

        Returns
        -------
        nbtlib.File
            An nbtlib.File object representing a default Chain Conveyor.
        """
        return create_conveyor_template()

    def add_connection(self, connection_pos: Union[Coord, ListType[Coord]]) -> None:
        """
        Adds one or more connection points to the Chain Conveyor's NBT data.

        Parameters
        ----------
        connection_pos : Union[Coord, ListType[Coord]]
            Either a single absolute coordinate [x, y, z] for a connection,
            or a list of absolute coordinates [[x1, y1, z1], [x2, y2, z2], ...].

        Returns
        -------
        None
        """
        positions = (
            connection_pos if isinstance(connection_pos[0], (list, tuple)) else [connection_pos]
        )

        for pos in positions:
            relative_pos = calculate_relative_pos(pos, self.origin)
            connection = IntArray([Int(x) for x in relative_pos])
            self.nbt['']['blocks'][0]['nbt']['Connections'].append(connection)


def generate_connected_conveyors(
    connections: Union[Coord, ListType[Coord]],
    origin: Optional[Coord] = None,
    base_filename: str = 'conveyor.nbt',
) -> None:
    """
    Generate and save NBT files for a main conveyor and its connected inverse conveyors.

    For each connection specified, this function creates an NBT file for the main
    conveyor with that connection, and a separate NBT file for the connected conveyor
    with an inverse connection pointing back to the main one.

    Parameters
    ----------
    connections : Union[Coord, ListType[Coord]]
        A single coordinate list/tuple [x, y, z] or a list of coordinates
        for the connections from the main conveyor.
    origin : Optional[Coord], optional
        The absolute world position [x, y, z] of the main conveyor.
        Defaults to [0, 0, 0].
    base_filename : str, optional
        The base filename for the saved NBT files. Suffixes like '_main.nbt'
        and '_1.nbt' will be added. Defaults to 'conveyor.nbt'.

    Returns
    -------
    None
    """
    origin_pos = list(origin) if origin else [0, 0, 0]
    conn_list = connections if isinstance(connections[0], (list, tuple)) else [connections]

    main_conveyor = ConveyorNBT(origin=origin_pos)
    for conn in conn_list:
        main_conveyor.add_connection(conn)
    main_conveyor.save(base_filename.replace('.nbt', '_main.nbt'))

    for i, conn in enumerate(conn_list, 1):
        inverse_origin = conn
        inverse_conn_target = origin_pos

        inv_conveyor = ConveyorNBT(origin=inverse_origin)
        inv_conveyor.add_connection(inverse_conn_target)
        inv_conveyor.save(base_filename.replace('.nbt', f'_{i}.nbt'))


# Example usage
if __name__ == '__main__':
    # Create ArmNBT with origin
    arm = ArmNBT(origin=[1, 1, 1])
    arm.add_interaction_point(type_str='create:depot', mode='TAKE', pos=[0, 0, 10])
    arm.add_interaction_point(type_str='create:depot', mode='DEPOSIT', pos=[0, 0, 11])

    # Create ConveyorNBT with  origin
    conveyor = ConveyorNBT(origin=[0, -63, 0])
    conveyor.add_connection([1000, 0, 0])  # Single coordinate
    conveyor.add_connection([[0, 1000, 0], [0, 0, 1000]])  # Multiple coordinates

    # Print results to verify
    print('Arm Interaction Points:')
    print(arm.nbt['']['blocks'][0]['nbt']['InteractionPoints'])
    print('\nConveyor Connections:')
    print(conveyor.nbt['']['blocks'][0]['nbt']['Connections'])

    # Example of saving the NBT files
    # arm.save('arm_example.nbt')
    # conveyor.save('conveyor_example.nbt')

    # Example of generating connected conveyor files
    # generate_connected_conveyors([10, -63, 0], origin=[0, -63, 0], base_filename='single_conn.nbt')
    # generate_connected_conveyors([[10, -63, 0], [0, -63, 10]], origin=[0, -63, 0], base_filename='multi_conn.nbt')
