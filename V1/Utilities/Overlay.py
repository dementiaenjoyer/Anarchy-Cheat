# TODO: add proper ingame check by ensuring that theres an address and port on 0xAB4D1 and 0xA9AB0. maybe compare previous server uptime value with current to check latest ping ?

from ctypes import ( windll as WinDLL, wintypes as WinTypes, c_ulong as CULong, c_bool as CBool, c_void_p as CVoidP, byref as Byref, WINFUNCTYPE as WinFunctionType, create_unicode_buffer as UnicodeBuffer );
from OpenGL.GL import ( glViewport as GraphicsViewport, glClearColor as GraphicsClearColor, glClear as GraphicsClear, GL_COLOR_BUFFER_BIT as GraphicsColorBufferBit );
from psutil import ( process_iter as ProcessIteration );
from struct import ( unpack as Unpack );
from threading import ( Thread );

import imgui as ImGui;
import glfw as Glfw;

from imgui.integrations.glfw import GlfwRenderer;

class Overlay:
    def __init__( Self, Process, Workspace ):
        Self.Workspace = Workspace;

        Self.Renderer = 0;
        Self.Window = 0;
        Self.InGame = 0;

        Self.Process = Process;
        Self.Callbacks = { };
    
        # Self.Initiate();

    def FindWindow( Self, ProcessHandle ):
        User32 = WinDLL.user32;
        Kernel32 = WinDLL.kernel32;

        PID = CULong( );
        Kernel32.GetProcessId( ProcessHandle );
        PID.value = Kernel32.GetProcessId( ProcessHandle );

        Result = CVoidP( None );

        @WinFunctionType( CBool, CVoidP, CVoidP )
        def Callback( HWND, *Arguments ):
            ProcessID = CULong( );
            User32.GetWindowThreadProcessId( HWND, Byref( ProcessID ) );

            if ( ProcessID.value != PID.value ) or ( not User32.IsWindowVisible( HWND ) ):
                return True;

            ClassName = UnicodeBuffer( 256 );
            User32.GetClassNameW( HWND, ClassName, 256 );

            if ( ClassName.value == "ConsoleWindowClass" ):
                return True;

            Result.value = HWND;

        User32.EnumWindows( Callback, 0 );

        return Result.value;

    def AddOverlay( Self ):
        if ( not Glfw.init( ) ):
            return;

        Hint = Glfw.window_hint;

        Hint( Glfw.OPENGL_PROFILE, Glfw.OPENGL_CORE_PROFILE );
        Hint( Glfw.TRANSPARENT_FRAMEBUFFER, True );
        Hint( Glfw.OPENGL_FORWARD_COMPAT, True );
        Hint( Glfw.CONTEXT_VERSION_MAJOR, 3 );
        Hint( Glfw.CONTEXT_VERSION_MINOR, 3 );
        Hint( Glfw.MOUSE_PASSTHROUGH, True );
        Hint( Glfw.SCALE_TO_MONITOR, False );
        Hint( Glfw.RESIZABLE, False );
        Hint( Glfw.DECORATED, False );
        Hint( Glfw.FLOATING, True );
        Hint( Glfw.FOCUSED, False );

        GameHandle = Self.FindWindow( Self.Process );

        if ( not GameHandle ):
            return;

        Window = Glfw.create_window( 1, 1, "", None, None );

        if ( not Window ):
            return;

        Glfw.make_context_current( Window );
        Glfw.swap_interval(1); # VSync ?

        User32 = WinDLL.user32;
        
        Handle = Glfw.get_win32_window( Window );
        Flags = User32.GetWindowLongW( Handle, -20 );

        User32.SetParent( Handle, GameHandle );
        User32.SetWindowLongW( Handle, -20, Flags | 134217728 );

        ImGui.create_context( );

        Renderer = GlfwRenderer( Window, False );
        Self.Renderer = Renderer;

        Rect = WinTypes.RECT( );
        
        Position = WinTypes.POINT( );
        Overlay = WinTypes.POINT( );

        WorkspaceObject = Self.Workspace;
        Self.Window = Window;

        while ( not Glfw.window_should_close( Window ) ):
            Dimensions = WorkspaceObject.Dimensions;

            Height = Dimensions.Y;
            Width = Dimensions.X;

            Glfw.set_window_size(Window, Width, Height);
            User32.SetWindowPos(Handle, None, 0, 0, 0, 0, 1 | 4 | 16); # SWP_NOSIZE, SWP_NOZORDER, SWP_NOACTIVATE

            WidthFrame, HeightFrame = Glfw.get_framebuffer_size( Window );
            Glfw.poll_events( );

            GraphicsViewport( 0, 0, WidthFrame, HeightFrame );
            GraphicsClearColor( 0, 0, 0, 0 );

            GraphicsClear( GraphicsColorBufferBit );

            Configuration = ImGui.get_io( );
            Configuration.display_size = ( WidthFrame, HeightFrame );

            User32.GetCursorPos( Byref( Position ) );

            Overlay.x = 0;
            Overlay.y = 0;

            User32.ClientToScreen( GameHandle, Byref( Overlay ) );

            Configuration.mouse_pos = (Position.x - Overlay.x, Position.y - Overlay.y); # relative mouse pos
            # print(Configuration.mouse_pos);
            
            MouseDown = Configuration.mouse_down;
            Activated = 32768;

            Left, Right = User32.GetAsyncKeyState( 0x01 ), User32.GetAsyncKeyState( 0x02 );

            MouseDown[0] = ( Left == Activated );
            MouseDown[1] = ( Right == Activated );

            ImGui.new_frame( );

            #if ( Self.InGame ):
            Self.Update( );
        
            ImGui.render( );
            Renderer.render(ImGui.get_draw_data( ));
        
            Glfw.swap_buffers( Window );

        Renderer.shutdown( );
        Glfw.terminate( );

    def AddJob( Self, Name, Callback ):
        Self.Callbacks[ Name ] = Callback;

    def Update( Self, *Arguments ):
        Renderer = Self.Renderer;
        Window = Self.Window;

        if ( not Renderer ) or ( not Window ):
            return;

        for Callback in Self.Callbacks.values( ):
            Callback( ImGui, *Arguments );

    def Initiate( Self ):
        Thread( target = Self.AddOverlay ).start( );