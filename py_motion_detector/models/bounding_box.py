class BoundingBox:
    def __init__(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    @property
    def area(self):
        return self.height * self.width

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def __repr__(self):
        return "{}(top={}, left={}, bottom={}, right={})".format(
            self.__class__.__name__, self.top, self.left, self.bottom, self.right)

    # TODO: use Marsmallow lib for serialization/deserialization
    def to_dict(self):
        return {
            "top": self.top,
            "left": self.left,
            "bottom": self.bottom,
            "right": self.right
        }

    @classmethod
    def from_dict(cls, dict_json):
        return cls(top=dict_json["top"], left=dict_json["left"], bottom=dict_json["bottom"], right=dict_json["right"])
