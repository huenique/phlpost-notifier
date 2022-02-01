"""
This type stub file was generated by pyright.
"""

__all__ = (
    "Type",
    "Attribute",
    "Range",
    "BitString",
    "Point",
    "Path",
    "Polygon",
    "Box",
    "Line",
    "LineSegment",
    "Circle",
    "ServerVersion",
)
Type = ...
Attribute = ...
ServerVersion = ...

class Range:
    """Immutable representation of PostgreSQL `range` type."""

    __slots__ = ...
    def __init__(
        self, lower=..., upper=..., *, lower_inc=..., upper_inc=..., empty=...
    ) -> None: ...
    @property
    def lower(self): ...
    @property
    def lower_inc(self): ...
    @property
    def lower_inf(self): ...
    @property
    def upper(self): ...
    @property
    def upper_inc(self): ...
    @property
    def upper_inf(self): ...
    @property
    def isempty(self): ...
    def issubset(self, other): ...
    def issuperset(self, other): ...
    def __bool__(self): ...
    def __eq__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self): ...
    __str__ = ...
