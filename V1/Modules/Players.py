from Classes . ReplicationObject import ( Class as ReplicationObject );
from Classes . PlayerObject import ( Class as PlayerObject );

from Dependencies . DataTypes import ( Vector3 );
from Utilities . Math import ( WorldToScreen );

from time import ( time as Tick );
from Utilities import ( Offsets );

class Class:
    def __init__( Self, MemoryObject ):
        Self.MemoryObject = MemoryObject;

        Self.Players = [ ];
        Self.Timestamp = 0;

    def GetClosestReplicator( Self, Range, Data ):
        ViewMatrix, Dimensions, Focal = Data; # i didn't really think about issues which could be encountered before going with this structure. for now, it'll be like this
        Closest, MaxDistance = ( None, None, None ), Range; # ( ReplicationObject, ScreenPosition, WorldPosition ), Range
    
        for Replicator in Self.GetReplicators( ):
            Position = Replicator.Position;
            W2S, OnScreen = WorldToScreen( Position = Position, ViewMatrix = ViewMatrix, Dimensions = Dimensions, Focal = Focal );

            if ( not OnScreen ):
                continue;
        
            Center = ( Dimensions * 0.5 );
            Distance = ( W2S - Center ).Magnitude;
        
            if ( Distance <= MaxDistance ):
                Closest = ( Replicator, W2S, Position );
                MaxDistance = Distance;

        return Closest;

    def GetReplicators( Self, Local = False, SpecificID = None ):
        Cache = Self.Players;
        Timestamp = Tick( );

        if ( not SpecificID ) and ( ( Timestamp - Self.Timestamp ) < 2 ) and len( Cache ) > 0:
            return Cache;

        Memory, Results = Self.MemoryObject, [ ];
        
        BaseAddress = Memory.BaseAddress;
        BaseOffsets = Offsets.Base;

        EntityList = Memory.ReadUInt64( BaseAddress + BaseOffsets.EntityList );
        EntityCount = Memory.ReadInt( BaseAddress + BaseOffsets.EntityCount );

        LocalID = Self.LocalID;

        for Index in range( EntityCount ):
            Address = EntityList + ( Index * 0x50 );
            UniqueID = Memory.ReadUInt32( Address );

            IsClient = ( UniqueID == LocalID );

            if ( UniqueID == 4294967295 ) or ( SpecificID and SpecificID != UniqueID ) or ( not Local and IsClient ):
                continue;

            Results.append( ( ( IsClient and PlayerObject ) or ReplicationObject )(
                MemoryObject = Memory, 
                Address = Address, 
                ID = UniqueID
            ));

        if ( not SpecificID ):
            Self.Timestamp = Timestamp;
            Self.Players = Results;

        return Results;

    @property
    def LocalID( Self ):
        MemoryObject = Self.MemoryObject;
        BaseOffsets = Offsets.Base;

        return MemoryObject.ReadUInt32( MemoryObject.BaseAddress + BaseOffsets.LocalID );

    @property
    def LocalPlayer( Self ):
        Result = Self.GetReplicators( Local = True, SpecificID = Self.LocalID );

        if ( len( Result ) > 0 ):
            Result = Result[ 0 ];

        return Result;

    @property
    def Size( Self ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        return MemoryObject.ReadDouble( BaseAddress + Offsets.Base.HitboxSize );

    @Size.setter
    def Size( Self, Value ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        MemoryObject.ForceWriteDouble( BaseAddress + Offsets.Base.HitboxSize, Value );

    @property
    def HeightOffset( Self ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        return MemoryObject.ReadDouble( BaseAddress + Offsets.Base.HeightOffset );

    @HeightOffset.setter
    def HeightOffset( Self, Value ):
        MemoryObject = Self.MemoryObject;
        BaseAddress = MemoryObject.BaseAddress;

        MemoryObject.ForceWriteDouble( BaseAddress + Offsets.Base.HeightOffset, Value );