from time import ( sleep as Sleep);
from threading import ( Thread );

class Schedular:
    def __init__( Self, Delay  = 0.01 ):
        Self.Callbacks = { };
        Self.Delay = Delay;

    def Initiate( Self ):
        def Stepper( ):
            while True: 
                Sleep( Self.Delay ); Self.Update( );
    
        return Thread( target = Stepper ).start( );

    def AddJob( Self, Name, Callback ):
        Self.Callbacks[ Name ] = Callback;

    def Update( Self ):
        for Callback in Self.Callbacks.values( ):
            Callback( );