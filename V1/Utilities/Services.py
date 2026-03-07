import importlib as ImportLibrary;

def GetService( Name, MemoryObject ):
    return ImportLibrary.import_module( "Modules." + Name ).Class( MemoryObject = MemoryObject );