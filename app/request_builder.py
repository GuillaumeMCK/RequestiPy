import customtkinter as ctk

import app.constants as constants
from app import Console
from utils.formatter import *


class RequestBuilder(ctk.CTkFrame):
    def __init__(self, master, console: Console, **kwargs):
        super().__init__(master, border_width=0, corner_radius=0, fg_color=colors.content2, **kwargs)
        self.console = console
        self._initialize_widgets()
        self._configure_grid()

    def _initialize_widgets(self):
        """Initialize and configure all widgets."""
        self._create_textbox_with_label("Header", self._create_header_tbx, row=0)
        self._create_textbox_with_label("Raw body", self._create_body_tbx, row=2)
        self._create_code_tbx()
        self._create_bottom_bar()

    def _create_textbox_with_label(self, label_text, create_textbox_func, row):
        """Creates a label and a corresponding textbox widget."""
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, sticky="w", pady=(0, 5), padx=5)
        create_textbox_func(row + 1)

    def _create_header_tbx(self, row):
        """Creates the header text box."""
        self.header_tbx = ctk.CTkTextbox(self, height=4, fg_color=colors.content3, bg_color=colors.content2)
        self.header_tbx.grid(row=row, column=0, sticky="nsew", padx=5, pady=(0, 5))
        self.header_tbx.insert("end", constants.req_header)
        self.header_tbx.bind("<KeyRelease>", lambda e: header_highlight(self.header_tbx))
        header_highlight(self.header_tbx)

    def _create_body_tbx(self, row):
        """Creates the body text box."""
        self.body_tbx = ctk.CTkTextbox(self, fg_color=colors.content3, bg_color=colors.content2)
        self.body_tbx.grid(row=row, column=0, sticky="nsew", padx=5)
        self.body_tbx.insert("end", constants.req_body)
        self.body_tbx.bind("<KeyRelease>", lambda e: body_highlight(self.body_tbx))
        body_highlight(self.body_tbx)

    def _create_code_tbx(self):
        """Creates the code editing frame."""
        self.code_tbx = ctk.CTkTextbox(self, height=4, fg_color=colors.content2, bg_color=colors.content2,
                                       border_color=colors.content3, border_width=2)
        self.code_tbx.grid(row=0, column=1, rowspan=6, sticky="nsew", pady=(5, 0), padx=(0, 5))
        self.code_tbx.bind("<KeyRelease>", lambda e: python_highlight(self.code_tbx))
        self.code_tbx.insert("end", constants.default_code)
        python_highlight(self.code_tbx)

    def _create_bottom_bar(self):
        """Creates the bottom control bar."""
        # self.topmost_switch = ctk.CTkSwitch(self, text="Stop on error")
        # self.topmost_switch.bind("<ButtonRelease-1>", lambda e: self.console.set_topmost(self.topmost_switch
        # self.topmost_switch.grid(row=6, column=0, sticky="w", padx=5)

        self.run_btn = ctk.CTkButton(self, text="Run", command=self.run_btn_cmd)
        self.run_btn.grid(row=6, column=1, sticky="e", padx=5)

        self.reset_btn = ctk.CTkButton(self, text="Reset", command=self.on_reset)
        self.reset_btn.grid(row=6, column=1, sticky="w", padx=5)

    def _configure_grid(self):
        """Configures grid layout for widgets."""
        for i in range(5):
            self.rowconfigure(i, weight=1 if i in {1, 3} else 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

    def on_reset(self):
        """Resets the request builder to its initial state."""
        self.header_tbx.delete("1.0", "end")
        self.body_tbx.delete("1.0", "end")
        self.code_tbx.delete("1.0", "end")

        self.header_tbx.insert("end", constants.req_header)
        self.body_tbx.insert("end", constants.req_body)
        self.code_tbx.insert("end", constants.default_code)

        body_highlight(self.body_tbx)
        header_highlight(self.header_tbx)
        python_highlight(self.code_tbx)

    def run_btn_cmd(self):
        """Executes the code present in the code frame."""
        code = self.code_tbx.get("1.0", "end").strip()
        header = self.header_tbx.get("1.0", "end").strip()
        body = self.body_tbx.get("1.0", "end").strip()

        self.run_btn.configure(state="disabled")
        try:
            self.console.info("Executing the code")
            exec(code, {}, {
                "console": self.console,
                "header": header,
                "body": None if not body else body,
            })
        except Exception as e:
            self.console.error(str(e))
        finally:
            self.run_btn.configure(state="normal")
