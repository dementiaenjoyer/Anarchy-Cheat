from math import ( atan2 as Atan2, sqrt as Sqrt, degrees as Degrees, radians as Radians );
from numpy.linalg import ( norm as Normalize );

from Dependencies.DataTypes import ( Vector2 );

def WorldToScreen( Position, ViewMatrix, Dimensions, Focal ):
    X, Y, Z = Position.X, Position.Y, Position.Z;
    Width, Height = Dimensions.X, Dimensions.Y;

    Row0 = ViewMatrix[ 0 ];
    Row1 = ViewMatrix[ 1 ];
    Row2 = ViewMatrix[ 2 ];

    Depth = ( X * Row2[ 0 ] + Y * Row2[ 1 ] + Z * Row2[ 2 ] + Row2[ 3 ] );

    if ( Depth > -0.1 ):
        return Vector2( 0, 0 ), False;

    HalfHeight = ( Height * 0.5 );
    HalfWidth = ( Width * 0.5 );

    ScreenY = ( HalfHeight ) - ( ( X * Row1[ 0 ] + Y * Row1[ 1 ] + Z * Row1[ 2 ] + Row1[ 3 ] ) / -Depth ) * Focal.Y * ( HalfHeight );
    ScreenX = ( HalfWidth ) + ( ( X * Row0[ 0 ] + Y * Row0[ 1 ] + Z * Row0[ 2 ] + Row0[ 3 ] ) / -Depth ) * Focal.X * ( HalfWidth );

    return Vector2( ScreenX, ScreenY ), True;

def WorldToAngle( Origin, Destination ):
    DeltaX = ( Destination.X - Origin.X );
    DeltaY = ( Destination.Y - Origin.Y );
    DeltaZ = ( Destination.Z - Origin.Z );

    Pitch = -Degrees( Atan2( DeltaZ, Sqrt( DeltaX ** 2 + DeltaY ** 2 ) ) );
    Yaw = ( Degrees( Atan2( -DeltaY, -DeltaX ) ) - 180 ) % 360;

    return Vector2( Pitch, Yaw );

OutlineOffsets = [ ( -1, 0 ), ( 1, 0 ), ( 0, -1 ), ( 0, 1 ), ( -1, -1 ), ( 1, -1 ), ( -1, 1 ), ( 1, 1 ) ];