from dataclasses import asdict, dataclass


@dataclass
class BoundingBox:
    """Defines the points of a bounding box."""

    top: int
    left: int
    bottom: int
    right: int

    @property
    def area(self):
        return self.height * self.width

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dict_json):
        return cls(**dict_json)
