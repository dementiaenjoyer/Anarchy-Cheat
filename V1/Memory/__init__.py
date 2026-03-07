from ctypes import ( c_void_p as CVoidP, byref as ByReference, wintypes as WinTypes, windll as WinDLL );
from pymem import ( Pymem );

Kernel32 = WinDLL.kernel32;

class PatternObject:
    def __init__( Self, Address, Length, MemoryObject ):
        Self.MemoryObject = MemoryObject;

        Self.Address = Address;
        Self.Length = Length;

    def NOP( Self ):
        MemoryObject = Self.MemoryObject;
        Address = Self.Address;
        Length = Self.Length;

        VirtualProtect = MemoryObject.VirtualProtectEx;

        VirtualProtect( Address, False, Length );
        MemoryObject.Game.write_bytes( Address, bytes( [ 0x90 ] * Length ), Length );
        VirtualProtect( Address, True, Length );

class Memory:
    def __init__( Self, Process = "ga1.exe" ):
        MemoryObject = Pymem( Process );

        Self.Handle = MemoryObject.process_handle;
        Self.Game = MemoryObject;

        Self.BaseAddress = MemoryObject.base_address;
        Self.ModifiedRegion = 0;

    # PATTERN
    def PatternEquals( Self, Module, Index, Bytes, Mask, Length ):
        for Offset in range( Length ):
            if ( not Mask[ Offset ] ):
                continue;
            
            if ( Module[ Index + Offset ] != Bytes[ Offset ] ):
                return;
    
        return True;

    def PatternScan( Self, Pattern, ModuleSize = 5242880 ):
        Parts, Index = Pattern.replace( " ", "" ), 0;
        Bytes, Mask = [ ], [ ];

        while ( Index < len( Parts ) ):
            Chunk = Parts[ Index : Index + 2 ];

            if ( Chunk == "??" ):
                Bytes.append( 0 ); Mask.append( False );
            else:
                Bytes.append( int( Chunk, 16 ) ); Mask.append( True );
            
            Index += 2;

        BaseAddress = Self.BaseAddress;
        
        Module = Self.ReadBytes( BaseAddress, ModuleSize );
        Length = len( Bytes );

        for Index in range( len( Module ) - Length ):
            if ( not Self.PatternEquals( Module, Index, Bytes, Mask, Length ) ):
                continue;

            return PatternObject( BaseAddress + Index, Length, Self );

    # SPECIAL
    def VirtualProtectEx( Self, Address, Restore, Size = 8 ):
        Previous = WinTypes.DWORD( 0 );
        Handle = Self.Handle;

        if ( not Restore ):
            Kernel32.VirtualProtectEx( Handle, CVoidP( Address ), Size, 64, ByReference( Previous ) );
            Self.ModifiedRegion = Previous.value;
            
            return;

        Kernel32.VirtualProtectEx( Handle, CVoidP( Address ), Size, Self.ModifiedRegion, ByReference( Previous ) );

    # INT16
    def WriteInt16( Self, Address, Value ):
        return Self.Game.write_short( Address, Value );

    def ReadInt16( Self, Address ):
        return Self.Game.read_short( Address );

    # INT32
    def WriteInt32( Self, Address, Value ):
        return Self.Game.write_long( Address, Value );

    def ReadInt32( Self, Address ):
        return Self.Game.read_long( Address );

    def ReadUInt32( Self, Address ):
        return Self.Game.read_uint( Address );

    def WriteUInt32( Self, Address, Value ):
        return Self.Game.write_uint( Address, Value );

    # INT64
    def WriteInt64( Self, Address, Value ):
        return Self.Game.write_longlong( Address, Value );

    def ReadInt64( Self, Address ):
        return Self.Game.read_longlong( Address );

    def WriteUInt64( Self, Address, Value ):
        return Self.Game.write_ulonglong( Address, Value );

    def ReadUInt64( Self, Address ):
        return Self.Game.read_ulonglong( Address );

    # FLOAT
    def ReadFloat( Self, Address ):
        return Self.Game.read_float( Address );

    def WriteFloat( Self, Address, Value ):
        return Self.Game.write_float( Address, float( Value ) );

    def ForceWriteFloat( Self, Address, Value ):
        Self.VirtualProtectEx( Address, False );
        Self.WriteFloat( Address, Value );

        Self.VirtualProtectEx( Address, True );

    # DOUBLE
    def ReadDouble( Self, Address ):
        return Self.Game.read_double( Address );

    def WriteDouble( Self, Address, Value ):
        return Self.Game.write_double( Address, float( Value ) );

    def ForceWriteDouble( Self, Address, Value ):
        Self.VirtualProtectEx( Address, False );
        Self.WriteDouble( Address, Value );

        Self.VirtualProtectEx( Address, True );

    # BOOL
    def ReadBool( Self, Address ):
        return Self.Game.read_bool( Address );

    def WriteBool( Self, Address, Value ):
        return Self.Game.write_bool( Address, Value );

    # INT
    def ReadInt( Self, Address ):
        return Self.Game.read_int( Address );

    # BYTES
    def ReadBytes( Self, Address, Length ):
        return Self.Game.read_bytes( Address, Length );