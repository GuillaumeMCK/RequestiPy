from os import path
from typing import Optional

import customtkinter as ctk
from PIL import Image

from models.colors import colors
from .console import Console
from .request_builder import RequestBuilder

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(path.join("assets", "theme.json"))

HEIGHT: int = 720
WIDTH: int = 1080
GITHUB_URL: str = "https://github.com/GuillaumeMCK/"


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.navbar: Optional[ctk.CTkFrame] = None
        self.console: Optional[Console] = None
        self.reqBuilder: Optional[RequestBuilder] = None
        self.setup_widgets()

    def setup_widgets(self) -> None:
        """Configure the main window and initialize widgets."""
        self._configure_window()
        self.navbar = self._create_navbar()
        self._add_control_buttons()
        self._initialize_console_and_request_builder()
        self._create_github_button()
        self._add_resize_button()
        self._configure_grid()

        self.console.log("$greeno/ $greyLogs viewer")

    def _configure_window(self) -> None:
        """Set up the main window attributes."""
        self.title("RequestiPy")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)

    def _create_navbar(self) -> ctk.CTkFrame:
        """Create and configure the navbar for the application."""
        navbar = ctk.CTkFrame(self, fg_color=colors.black, height=38)
        navbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        icon = ctk.CTkImage(dark_image=Image.open("icon.ico"))
        ctk.CTkLabel(navbar, text="RequestiPy", image=icon, compound="left", fg_color=colors.black,
                     bg_color=colors.black).grid(row=0, column=0, sticky="w", padx=5)
        navbar.bind("<B1-Motion>", self._drag_window)
        return navbar

    def _add_resize_button(self):
        """Add a resize button to the bottom right corner of the window."""
        corner_right = ctk.CTkFrame(self, width=2, height=25, fg_color=colors.grey, bg_color=colors.grey)
        corner_right.bind("<B1-Motion>", self._resize_height_width)
        corner_right.grid(row=1, column=0, sticky="se", columnspan=2)

        corner_bottom = ctk.CTkFrame(self, width=25, height=2, fg_color=colors.grey, bg_color=colors.grey)
        corner_bottom.bind("<B1-Motion>", self._resize_height_width)
        corner_bottom.grid(row=1, column=0, sticky="se", columnspan=2)

    def _resize_height_width(self, event) -> None:
        """Handle window resizing."""
        current_width = event.x_root - self.winfo_x()
        current_height = event.y_root - self.winfo_y()

        if current_width and current_height:
            self.geometry(f"{current_width}x{current_height}")

    def _drag_window(self, event) -> None:
        """Handle window dragging."""
        self.geometry(f"+{event.x_root - self.winfo_width() // 2}+{event.y_root - self.navbar.winfo_height() // 2}")

    def _add_control_buttons(self) -> None:
        """Add close, maximize, and minimize buttons to the navbar."""
        buttons_config = [
            {"text": "-", "command": self._minimize},
            {"text": "□", "command": self._maximize},
            {"text": "×", "command": self.destroy, "color": colors.red},
        ]

        for index, config in enumerate(buttons_config):
            self._create_button(config["text"], config["command"], index + 1, config.get("color"))

    def _minimize(self) -> None:
        self.overrideredirect(False)
        self.state("iconic")
        self.overrideredirect(True)

    def _maximize(self) -> None:
        self.overrideredirect(False)
        if self.state() == "zoomed":
            self.state("normal")
            self.overrideredirect(True)
        else:
            self.state("zoomed")

    def _create_button(self, text: str, command: callable, column: int, color: Optional[str] = None) -> None:
        """Create a control button for the navbar."""
        button_color = colors.grey if color is None else color
        button = ctk.CTkButton(
            self.navbar,
            text=text,
            width=30,
            fg_color=colors.lerp(colors.black, button_color, 0.1 if button_color != colors.grey else 0.0),
            hover_color=colors.lerp(colors.black, button_color, 0.12),
            text_color=button_color,
            border_color=colors.black,
            border_width=0,
            corner_radius=0,
            command=command
        )
        button.grid(row=0, column=column, sticky="e")

    def _initialize_console_and_request_builder(self) -> None:
        """Initialize the console and request builder."""
        self.console = Console(self)
        self.console.grid(row=1, column=1, sticky="nswe", padx=(0, 2), pady=(0, 2))

        self.reqBuilder = RequestBuilder(self, console=self.console)
        self.reqBuilder.grid(row=1, column=0, sticky="nsew", padx=(2, 0), pady=(0, 2))

    def _create_github_button(self) -> None:
        """Create and place the GitHub button."""
        gh_logo = ctk.CTkImage(dark_image=Image.open(path.join("assets", "github.png")))
        self.gh_button = ctk.CTkButton(
            self,
            text="",
            image=gh_logo,
            command=None,
            width=32,
            height=32,
            bg_color=colors.content1,
            fg_color=colors.content1
        )
        self.gh_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=43)

    def _configure_grid(self) -> None:
        """Set up grid configuration for layout management."""
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.navbar.columnconfigure(0, weight=1)


def start() -> None:
    """Start the application."""
    app = App()
    app.overrideredirect(True)
    app.focus_force()
    app.attributes("-alpha", 1)
    app.mainloop()
