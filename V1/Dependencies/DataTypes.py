"""
warning: gpt gave me these, i only slightly modified them. if the code looks worse than normal, that is why.
"""

from math import ( sqrt as Sqrt );

class Vector3:
    def __init__( Self, X = 0, Y = 0, Z = 0 ):
        Self.X = X;
        Self.Y = Y;
        Self.Z = Z;

    def __repr__( Self ):
        return f"Vector3({ Self.X }, {Self.Y }, {Self.Z })";

    def __str__( Self ):
        return f"({ Self.X }, { Self.Y }, {Self.Z })";

    def __add__( Self, Value ):
        return Vector3( Self.X + Value.X, Self.Y + Value.Y, Self.Z + Value.Z );

    def __sub__( Self, Value ):
        return Vector3( Self.X - Value.X, Self.Y - Value.Y, Self.Z - Value.Z );

    def __mul__( Self, Scalar ):
        return Vector3( Self.X * Scalar, Self.Y * Scalar, Self.Z * Scalar );

    def __rmul__( Self, Scalar ):
        return Self.__mul__( Scalar );

    def __truediv__( Self, Scalar ):
        return Vector3( Self.X / Scalar, Self.Y / Scalar, Self.Z / Scalar );

    def __neg__( Self ):
        return Vector3( -Self.X, -Self.Y, -Self.Z );

    @property
    def Magnitude( Self ):
        return Sqrt( Self.X ** 2 + Self.Y ** 2 + Self.Z ** 2 );

class Vector2:
    def __init__( Self, X = 0, Y = 0 ):
        Self.X = X;
        Self.Y = Y;

    def __repr__( Self ):
        return f"Vector2({ Self.X }, { Self.Y })";

    def __str__( Self ):
        return f"({ Self.X }, { Self.Y} )";

    def __add__( Self, Value ):
        return Vector2( Self.X + Value.X, Self.Y + Value.Y );

    def __sub__( Self, Value ):
        return Vector2( Self.X - Value.X, Self.Y - Value.Y );

    def __mul__( Self, Scalar ):
        return Vector2( Self.X * Scalar, Self.Y * Scalar );

    def __rmul__( Self, Scalar ):
        return Self.__mul__( Scalar );

    def __truediv__( Self, Scalar ):
        return Vector2( Self.X / Scalar, Self.Y / Scalar );

    def __neg__( Self ):
        return Vector2( -Self.X, -Self.Y );

    @property
    def Magnitude( Self ):
        return Sqrt( Self.X ** 2 + Self.Y ** 2 );