class Colors:
    def __init__(self):
        self.white = "#FFFFFF"
        self.black = "#000000"
        self.red = "#FF2548"
        self.green = "#9FEF00"
        self.blue = "#0086FF"
        self.orange = "#FFAF00"
        self.yellow = "#FFD800"
        self.magenta = "#986CE8"
        self.purple = "#6C5CE7"
        self.pink = "#FF5C8D"
        self.grey = "#A4B1CD"
        self.content1 = "#111927"
        self.content2 = "#141D2B"
        self.content3 = "#1A2332"
        self.content4 = "#202837"

    def to_dict(self):
        values = {k: v for k, v in vars(self).items() if not k.startswith("__")}
        return {f"${k}": v for k, v in values.items()}

    def __getitem__(self, item):
        return self.to_dict().get(item)

    def __iter__(self):
        return iter(self.to_dict())

    def lerp(self, color1, color2, t):
        """Linear interpolation between two colors."""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)

        r = int(r1 + t * (r2 - r1))
        g = int(g1 + t * (g2 - g1))
        b = int(b1 + t * (b2 - b1))

        return f"#{r:02X}{g:02X}{b:02X}"

    def _hex_to_rgb(self, color):
        """Converts a color from hexadecimal to RGB."""
        color = color.lstrip("#")
        return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


colors = Colors()
