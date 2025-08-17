import nbtlib
from nbtlib.tag import Compound, List, Int, IntArray, Float, String, Byte


def create_arm_template():
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


def create_conveyor_template():
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


def calculate_relative_pos(pos, origin):
    """
    Calculate relative position by subtracting origin from position.

    Args:
        pos: List or tuple of three integers [x, y, z]
        origin: List or tuple of three integers [x, y, z]

    Returns:
        List of relative coordinates [x, y, z]
    """
    return [p - o for p, o in zip(pos, origin)]


class ArmNBT:
    def __init__(self, origin=None):
        """
        Initialize ArmNBT with optional origin.

        Args:
            origin: List or tuple of three integers for the origin [x, y, z]. Default [0, 0, 0].
        """
        self.origin = origin or [0, 0, 0]
        self.nbt = create_arm_template()

    def add_interaction_point(self, type_str, mode, pos):
        """
        Add an InteractionPoint to the arm NBT.

        Args:
            type_str: String for the Type field (e.g., 'create:depot')
            mode: String for the Mode field ('TAKE' or 'DEPOSIT')
            pos: List or tuple of three integers for the absolute position [x, y, z]
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

    def save(self, filename):
        """
        Save the NBT data to a file.

        Args:
            filename: String for the filename to save as.
        """
        self.nbt.save(filename,gzipped=True)


class ConveyorNBT:
    def __init__(self, origin=None):
        """
        Initialize ConveyorNBT with optional origin.

        Args:
            origin: List or tuple of three integers for the origin [x, y, z]. Default [0, 0, 0].
        """
        self.origin = origin or [0, 0, 0]
        self.nbt = create_conveyor_template()

    def add_connection(self, connection_pos):
        """
        Add one or multiple Connections to the conveyor NBT.

        Args:
            connection_pos: Either a single list/tuple of three integers [x, y, z]
                          or a list of lists/tuples, each with three integers
        """
        if isinstance(connection_pos[0], (list, tuple)):
            for pos in connection_pos:
                relative_pos = calculate_relative_pos(pos, self.origin)
                connection = IntArray([Int(x) for x in relative_pos])
                self.nbt['']['blocks'][0]['nbt']['Connections'].append(connection)
        else:
            relative_pos = calculate_relative_pos(connection_pos, self.origin)
            connection = IntArray([Int(x) for x in relative_pos])
            self.nbt['']['blocks'][0]['nbt']['Connections'].append(connection)

    def save(self, filename):
        """
        Save the NBT data to a file.

        Args:
            filename: String for the filename to save as.
        """
        self.nbt.save(filename,gzipped=True)


def generate_connected_conveyors(connections, origin=None, base_filename='conveyor.nbt'):
    """
    Generate and save NBT files for a main conveyor and its connected inverse conveyors.

    Args:
        connections: Either a single list/tuple of three integers [x, y, z]
                     or a list of lists/tuples, each with three integers
        origin: Optional origin [x, y, z]. Default [0, 0, 0].
        base_filename: Base filename for saving NBT files. Default 'conveyor.nbt'.
    """
    main = ConveyorNBT(origin=origin)
    main.add_connection(connections)
    main.save(base_filename.replace('.nbt', '_main.nbt'))

    # Convert single coordinate to list of coordinates for consistent processing
    conn_list = [connections] if isinstance(connections[0], (int, float)) else connections
    for i, conn in enumerate(conn_list, 1):
        inverse_conn = [-x for x in conn]
        inv_conveyor = ConveyorNBT(origin=origin)
        inv_conveyor.add_connection(inverse_conn)
        inv_conveyor.save(base_filename.replace('.nbt', f'_{i}.nbt'))


# Example usage
if __name__ == '__main__':
    # Create ArmNBT with origin
    arm = ArmNBT(origin=[1, 1, 1])
    arm.add_interaction_point(type_str='create:depot', mode='TAKE', pos=[0, 0, 10])

    arm.add_interaction_point(type_str='create:depot', mode='DEPOSIT', pos=[0, 0, 11])

    # Create ConveyorNBT with default origin
    conveyor = ConveyorNBT(origin=[0, -63, 0])
    conveyor.add_connection([1000, 0, 0])  # Single coordinate
    conveyor.add_connection([[0, 1000, 0], [0, 0, 1000]])  # Multiple coordinates

    # Print results
    print(arm.nbt['']['blocks'][0]['nbt']['InteractionPoints'])
    print(conveyor.nbt['']['blocks'][0]['nbt']['Connections'])

    # Example save
    # arm.save('arm_example.nbt')
    # conveyor.save('conveyor_example.nbt')

    # Example generate connected conveyors with single or multiple coordinates
    # generate_connected_conveyors([0, 1000, 0])  # Single coordinate
    # generate_connected_conveyors([[0, 1000, 0], [0, 0, 1000]])  # Multiple coordinates
