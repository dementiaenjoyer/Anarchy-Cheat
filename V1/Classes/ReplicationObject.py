from Utilities.Offsets import ( Base as Offsets );
from Dependencies.DataTypes import ( Vector3 );

class Class:
    def __init__( Self, MemoryObject, Address, ID ):
        Self.MemoryObject = MemoryObject;
        Self.Address = Address
        Self.ID = ID;

    @property
    def Position( Self ):
        MemoryObject = Self.MemoryObject;
        Address = Self.Address;

        ReadDouble = MemoryObject.ReadDouble;
        
        X = ReadDouble( Address = Address + 0x08 );
        Y = ReadDouble( Address = Address + 0x10 );
        Z = ReadDouble( Address = Address + 0x18 );

        return Vector3( X = X, Y = Y, Z = Z );

    @Position.setter
    def Position( Self, Value ):
        MemoryObject = Self.MemoryObject;
        Address = Self.Address;

        X = Value.X;
        Y = Value.Y;
        Z = Value.Z;

        WriteDouble = MemoryObject.WriteDouble;

        WriteDouble( Address = Address + 0x08, Value = X );
        WriteDouble( Address = Address + 0x10, Value = Y );
        WriteDouble( Address = Address + 0x18, Value = Z );

    @property
    def Name( Self ):
        return "Player " + str( Self.ID );