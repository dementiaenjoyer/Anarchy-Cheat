from Classes.ReplicationObject import ( Class as ReplicationObject );
from Utilities.Offsets import ( Base as Offsets );

class Class( ReplicationObject ): # this is a seperate class from ReplicationObject because of the way i decided to get offsets / addresses. will most likely change this in the future.
    def __init__( Self, MemoryObject, Address, ID ):
        Self.MemoryObject = MemoryObject;
        Self.Address = Address
        Self.ID = ID;
    
    @property
    def WalkSpeed( Self ):
        return Self.MemoryObject.ReadFloat( Self.MemoryObject.BaseAddress + Offsets.WalkSpeed );

    @WalkSpeed.setter
    def WalkSpeed( Self, Value ):
        Self.MemoryObject.WriteFloat( Self.MemoryObject.BaseAddress + Offsets.WalkSpeed, Value );