from Utilities.Offsets import ( Base as Offsets );
from Utilities.Math import ( WorldToAngle );

from Dependencies.DataTypes import ( Vector3, Vector2 );
from numpy import ( array as Array, zeros as Zeros );

class Class:
    def __init__( Self, MemoryObject ):
        Self.MemoryObject = MemoryObject

    def GetViewMatrix( Self ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        RawData = [ MemoryObject.ReadDouble( ( BaseAddress + Offsets.ViewMatrix ) + ( Index * 8 ) ) for Index in range( 16 ) ];

        ViewMatrix = Zeros( ( 4, 4 ) );
        ViewMatrix[ : ] = [ RawData[ Index : Index + 4 ] for Index in range( 0, 16, 4 ) ];

        return ViewMatrix.transpose( );

    def GetFocal( Self ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        FocalX = MemoryObject.ReadDouble( BaseAddress + Offsets.FocalX );
        FocalY = MemoryObject.ReadDouble( BaseAddress + Offsets.FocalY );

        return Vector2( X = FocalX, Y = FocalY );

    def LookAt( Self, Origin, Destination ):
        Angle = WorldToAngle( Origin, Destination );
        # print(Angle.X, Angle.Y);

        Self.Pitch = Angle.X;
        Self.Yaw = Angle.Y;

    @property
    def Yaw( Self ):
        MemoryObject = Self.MemoryObject;

        return MemoryObject.ReadDouble( MemoryObject.BaseAddress + Offsets.CameraYaw );

    @Yaw.setter
    def Yaw( Self, Value ):
        MemoryObject = Self.MemoryObject;

        MemoryObject.WriteDouble( MemoryObject.BaseAddress + Offsets.CameraYaw, Value );

    @property
    def Pitch( Self ):
        MemoryObject = Self.MemoryObject;

        return MemoryObject.ReadDouble( MemoryObject.BaseAddress + Offsets.CameraPitch );

    @Pitch.setter
    def Pitch( Self, Value ):
        MemoryObject = Self.MemoryObject;

        MemoryObject.WriteDouble( MemoryObject.BaseAddress + Offsets.CameraPitch, Value );

    @property
    def LookVector( Self ):
        MemoryObject = Self.MemoryObject
        ReadDouble = MemoryObject.ReadDouble

        Address = MemoryObject.BaseAddress + Offsets.LookVector;

        X = ReadDouble(Address = Address + 0x00);
        Y = ReadDouble(Address = Address + 0x08);
        Z = ReadDouble(Address = Address + 0x10);

        return Vector3(X = X, Y = Y, Z = Z);

    @property
    def FieldOfView( Self ):
        MemoryObject = Self.MemoryObject;

        return MemoryObject.ReadDouble( MemoryObject.BaseAddress + Offsets.CurrentFOV );

    @FieldOfView.setter
    def FieldOfView( Self, Value ):
        MemoryObject = Self.MemoryObject;

        MemoryObject.WriteDouble( MemoryObject.BaseAddress + Offsets.CurrentFOV, Value );

    @property
    def BaseFieldOfView( Self ):
        MemoryObject = Self.MemoryObject;

        return MemoryObject.ReadDouble( MemoryObject.BaseAddress + Offsets.BaseFOV );

    @FieldOfView.setter
    def BaseFieldOfView( Self, Value ):
        MemoryObject = Self.MemoryObject;

        MemoryObject.WriteDouble( MemoryObject.BaseAddress + Offsets.BaseFOV, Value );