from Utilities.Offsets import ( Base as Offsets );
from Dependencies.DataTypes import ( Vector2 );

import Classes.CameraObject as CameraObject;

class Class:
    def __init__( Self, MemoryObject ):
        Self.MemoryObject = MemoryObject;
        Self.Camera = None;

    @property
    def CurrentCamera( Self ):
        CachedObject = Self.Camera or CameraObject.Class( MemoryObject = Self.MemoryObject );
        Self.Camera = CachedObject;

        return CachedObject;

    @property
    def Dimensions( Self ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        Height = MemoryObject.ReadInt( BaseAddress + Offsets.Height );
        Width = MemoryObject.ReadInt( BaseAddress + Offsets.Width );

        return Vector2( X = Width, Y = Height );

    @Dimensions.setter
    def Dimensions( Self, Value ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        MemoryObject.WriteInt( BaseAddress + Offsets.Height, Value.Y );
        MemoryObject.WriteInt( BaseAddress + Offsets.Width, Value.X );