from Dependencies.DataTypes import ( Vector3 );

from Utilities.Math import ( WorldToScreen, OutlineOffsets, WorldToAngle );
from Utilities.Offsets import ( Base as Offsets );
from Utilities.Schedular import ( Schedular );
from Utilities.Services import ( GetService );
from Utilities.Overlay import ( Overlay );

from win32api import ( GetAsyncKeyState );
from Memory import ( Memory );

MemoryObject = Memory( Process = "ga1.exe" );

Replication = GetService( Name = "Players", MemoryObject = MemoryObject );
Workspace = GetService( Name = "Workspace", MemoryObject = MemoryObject );

CurrentCamera = Workspace.CurrentCamera;
LocalPlayer = Replication.LocalPlayer;

class JaredHack:
    def __init__( Self ):
        Self.Options = {
            "Combat": { "Aimbot": False, "Silent Aim": False, "Hitbox Expander": False }, 
            "Visuals": { "ESP": { "Box": False, "Name": False }, "Weapon Transparency": False  }
        };

        Self.ViewMatrix = 0;
        Self.Position = 0;
        Self.Target = 0;

    # Cheat
    def DeleteInstruction( Self ):
        PatternScan = MemoryObject.PatternScan;

        # WeaponAngle = PatternScan( "F3 0F 10 15 EE 68 09 00" );

        RecoilX = PatternScan( "F3 0F11 05 52 6F 09 00" );
        RecoilY = PatternScan( "F3 0F11 05 28 6F 09 00" );
        RecoilZ = PatternScan( "0F11 0D ED 6F 09 00" );

        Sway = PatternScan( "F3 0F11 05 76 6F 09 00" );

        try: # since wwe NOP these here, we shnould be able to write to them for silent aim - im a genius (it worked)
            RecoilX.NOP( );
            RecoilY.NOP( );
            RecoilZ.NOP( );

            Sway.NOP( );
        except Exception:
            print( "deleteinstruction function errored, this is most likely because the instructions were already nopped." );

    def Update( Self ):
        ViewMatrix = CurrentCamera.GetViewMatrix( );
        Focal = CurrentCamera.GetFocal( );

        Dimensions = Workspace.Dimensions;
        Position =  LocalPlayer.Position;

        Self.ViewMatrix = ViewMatrix;
        Self.Position = Position;
        Self.Focal = Focal;
    
        Self.Target = Replication.GetClosestReplicator( Range = float( "inf" ), Data = ( ViewMatrix, Dimensions, Focal ) );

    def Initiate( Self ):
        Self.DeleteInstruction( );

        SchedularObject.AddJob( "Globals", Self.Update );
        
        SchedularObject.AddJob( "Weapon Transparency", Self.WeaponTransparency );
        SchedularObject.AddJob( "Hitbox Expander", Self.ExpandHitbox );
        SchedularObject.AddJob( "Silent Aim", Self.SilentAim );
        SchedularObject.AddJob( "Aimbot", Self.Aimbot );

        OverlayObject.AddJob( "Interface", Self.Interface );
        OverlayObject.AddJob( "ESP", Self.ESP );

        SchedularObject.AddJob( "Movement", Self.Movement );

    # Rendering
    def Interface( Self, ImGui, *Arguments ):
        ImGui.begin( "jaredhack" );
        
        VisualsOptions = Self.Options[ "Visuals" ];
        CombatOptions = Self.Options[ "Combat" ];

        HBConfig = CombatOptions[ "Hitbox Expander" ];
        SAConfig = CombatOptions[ "Silent Aim" ];
        ATConfig = CombatOptions[ "Aimbot" ];

        TWConfig = VisualsOptions[ "Weapon Transparency" ];
        EPConfig = VisualsOptions[ "ESP" ];

        Checkbox = ImGui.checkbox;

        BeginTabItem = ImGui.begin_tab_item;
        BeginTabBar = ImGui.begin_tab_bar;

        EndTabItem = ImGui.end_tab_item;
        EndTabBar = ImGui.end_tab_bar;

        if ( BeginTabBar( "Features" ) ):
            if ( BeginTabItem( "Combat" ).selected ):
                HBEnabled, HBValue = Checkbox( "Hitbox Expander", HBConfig );
                SAEnabled, SAValue = Checkbox( "Silent Aim", SAConfig );
                ATEnabled, ATValue = Checkbox( "Aimbot", ATConfig );

                # i'll find a better way to do this later
                if ( HBEnabled ):
                    CombatOptions[ "Hitbox Expander" ] = HBValue;

                if ( SAEnabled ):
                    CombatOptions[ "Silent Aim" ] = SAValue;

                if ( ATEnabled ):
                    CombatOptions[ "Aimbot" ] = ATValue;

                EndTabItem( );

            if ( BeginTabItem( "Visuals" ).selected ):
                TWEnabled, TWValue = Checkbox( "Invisible Weapon", TWConfig );

                if ( TWEnabled ):
                    VisualsOptions[ "Weapon Transparency" ] = TWValue;

                EndTabItem( );
            
            if ( BeginTabItem( "Players" ).selected ):
                NameEnabled, NameValue = Checkbox( "Name", EPConfig[  "Name" ] );
                BoxEnabled, BoxValue = Checkbox( "Box", EPConfig[ "Box" ] );

                if ( NameEnabled ):
                    EPConfig[ "Name" ] = NameValue;

                if ( BoxEnabled ):
                    EPConfig[ "Box" ] = BoxValue;

                EndTabItem( );

            EndTabBar( );

        ImGui.end( );

    def ESP( Self, ImGui, *Arguments ):
        DrawList = ImGui.get_background_draw_list( );

        CameraPosition = Self.Position;
        Focal = Self.Focal;

        U32RGBA = ImGui.get_color_u32_rgba;

        Black = U32RGBA( 0, 0, 0, 1 );
        White = U32RGBA( 1, 1, 1, 1 );

        ESPOptions = Self.Options[ "Visuals" ][ "ESP" ];

        for Entity in Replication.GetReplicators( ):
            FieldOfView = CurrentCamera.FieldOfView;
            Dimensions = Workspace.Dimensions;
            ViewMatrix = Self.ViewMatrix;

            Position = Entity.Position;

            X = Position.X;
            Y = Position.Y;
            Z = Position.Z;

            SizeOffset = 2;

            Bottom, _ = WorldToScreen( Vector3( X, Y, Z - ( SizeOffset * 7 ) ), ViewMatrix, Dimensions, Focal );
            Top, OnScreen = WorldToScreen( Vector3( X, Y, Z + 2 ), ViewMatrix, Dimensions, Focal );

            if ( not OnScreen ):
                continue;

            BottomX = Bottom.X;
            BottomY = Bottom.Y;

            TopX = Top.X;
            TopY = Top.Y;

            BoxHeight = abs( BottomY - TopY );
            HalfHeight = ( BoxHeight * 0.5 );

            BoxWidth = ( BoxHeight * 0.3 );
            HalfWidth = ( BoxWidth * 0.5 );

            CenterX = round( ( TopX + BottomX ) * 0.5 );
            CenterY = round( ( TopY + BottomY ) * 0.5 );

            Bottom = round( CenterY + HalfHeight );
            Top = round( CenterY - HalfHeight );

            Right = round( CenterX + HalfWidth );
            Left = round( CenterX - HalfWidth );

            AddRectangle = DrawList.add_rect;
            AddText = DrawList.add_text;

            Distance = ( Position - CameraPosition ).Magnitude;
            Size = max( 1, min( 2, round( 50 / Distance ) ) );

            if ( ESPOptions[ "Box" ] ):
                AddRectangle( Left - Size, Top - Size, Right + Size, Bottom + Size, Black, 0, 0, 1 );
                AddRectangle( Left, Top, Right, Bottom, White, 0, 0, 1 );
                AddRectangle( Left + Size, Top + Size, Right - Size, Bottom - Size, Black, 0, 0, 1 );

            if ( ESPOptions[ "Name" ] ):
                Text = Entity.Name;

                CenterX = round( CenterX - ( ImGui.calc_text_size( Text )[ 0 ] ) * 0.5 );
                Top = ( Top - 17 );

                for OffsetX, OffsetY in OutlineOffsets:
                    AddText( CenterX + OffsetX, Top + OffsetY, Black, Text );

                AddText( CenterX, Top, White, Text );

    def WeaponTransparency( Self ):
        Value = 255;

        if ( Self.Options[ "Visuals" ][ "Weapon Transparency" ] ):
            Value = 0;

        MemoryObject.ForceWriteFloat( MemoryObject.BaseAddress + Offsets.WeaponTransparency, Value );

    # Combat
    def Aimbot( Self ):
        if ( not Self.Options[ "Combat" ][ "Aimbot" ] ) or ( not GetAsyncKeyState( 0x02 ) ):
            return;
    
        ClosestPlayer = Self.Target;

        if ( not ClosestPlayer ):
            return;

        Position = ClosestPlayer[ 2 ];

        if ( not Position ):
            return;
    
        CurrentCamera.LookAt( Self.Position, Position );
    
    def SilentAim( Self ):
        if ( not Self.Options[ "Combat" ][ "Silent Aim" ] ):
            return;

        BaseAddress = MemoryObject.BaseAddress;
        ClosestPlayer = Self.Target;

        if ( not ClosestPlayer ):
            return;

        Position = ClosestPlayer[ 2 ];

        if ( not Position ):
            return;

        Angle = WorldToAngle( Self.Position, Position );

        CurrentPitch = CurrentCamera.Pitch;
        CurrentYaw = CurrentCamera.Yaw;

        WriteFloat = MemoryObject.WriteFloat;

        WriteFloat( BaseAddress + Offsets.RecoilX, ( Angle.X - CurrentPitch + 90 ) % 180 - 90 );
        WriteFloat( BaseAddress + Offsets.RecoilY, ( Angle.Y - CurrentYaw + 180 ) % 360 - 180 );

    def ExpandHitbox( Self ):
        Replication.Size = ( Self.Options[ "Combat" ][ "Hitbox Expander" ] and 3 ) or 0.5;

    # Misc
    def Movement( Self ):
        LocalPlayer.WalkSpeed = 128;
        #MemoryObject.WriteDouble(  )

OverlayObject = Overlay( Process = MemoryObject.Handle, Workspace = Workspace );
SchedularObject = Schedular( Delay = 0.01 );

CheatObject = JaredHack( );

SchedularObject.Initiate( );
OverlayObject.Initiate( );
CheatObject.Initiate( );

print("[jaredhack] get to pwning !");