import customtkinter as ctk

import app.constants as constants
from app import Console
from utils.highlighter import *


class RequestBuilder(ctk.CTkFrame):
    def __init__(self, master, console: Console, **kwargs):
        super().__init__(master, border_width=0, corner_radius=0, fg_color=colors.content2, **kwargs)
        self.console = console
        self._initialize_widgets()
        self._configure_grid()

    def _initialize_widgets(self):
        """Initialize and configure all widgets."""
        self._create_textbox_with_label("Header & Body", self._create_request_tbx, row=0)  # Merged header and body
        self._create_code_tbx()
        self._create_bottom_bar()

    def _create_textbox_with_label(self, label_text, create_textbox_func, row):
        """Creates a label and a corresponding textbox widget."""
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, sticky="w", pady=(0, 5), padx=5)
        create_textbox_func(row + 1)

    def _create_request_tbx(self, row):
        """Creates a request text box for both header and body."""
        self.request_tbx = ctk.CTkTextbox(self, fg_color=colors.content3, bg_color=colors.content2)
        self.request_tbx.grid(row=row, column=0, sticky="nsew", padx=5)
        self.request_tbx.insert("end",
                                constants.req_header + "\n\n" + constants.req_body)  # Insert both header and body
        self.request_tbx.bind("<KeyRelease>", lambda e: self._highlight_request_tbx())
        self._highlight_request_tbx()

    def _highlight_request_tbx(self):
        """Applies syntax highlighting for the request textbox."""
        vars_highlight(self.request_tbx)
        header_highlight(self.request_tbx)

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
        self.topmost_switch = ctk.CTkSwitch(self, text="Topmost", command=self.toggle_topmost)
        self.topmost_switch.grid(row=6, column=0, sticky="w", padx=5)

        self.run_btn = ctk.CTkButton(self, text="Run", command=self.run_btn_cmd)
        self.run_btn.grid(row=6, column=1, sticky="e", padx=5)

        self.reset_btn = ctk.CTkButton(self, text="Reset", command=self.on_reset)
        self.reset_btn.grid(row=6, column=1, sticky="w", padx=5)

    def _configure_grid(self):
        """Configures grid layout for widgets."""
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

    def on_reset(self):
        """Resets the request builder to its initial state."""
        self.request_tbx.delete("1.0", "end")
        self.request_tbx.insert("end", constants.req_header + "\n\n" + constants.req_body)
        self._highlight_request_tbx()
        self.code_tbx.delete("1.0", "end")
        self.code_tbx.insert("end", constants.default_code)
        python_highlight(self.code_tbx)

    def run_btn_cmd(self):
        """Executes the code present in the code frame."""
        code = self.code_tbx.get("1.0", "end").strip()
        request_content = self.request_tbx.get("1.0", "end").strip()

        if "\n\n" in request_content:
            header, body = request_content.split("\n\n", 1)
        else:
            header, body = request_content, ""

        reg = re.compile(r"§(.*?)§")
        vars = reg.findall(header + body)
        vars = list(set(vars))
        if not vars:
            self.console.warning("No variables found in the header or body")

        code = constants.helpers_code + code
        code = "def main(header: str, body: str, console: object, args):\n    " + code.replace("\n", "\n    ")
        code += "\nmain(header, body, console, args)"

        self.run_btn.configure(state="disabled")
        try:
            self.console.draw_line()
            self.console.info("Executing the code")
            self.console.log("Header:\n" + header)
            self.console.log("Body:\n" + body[:80] + "..." if len(body) > 25 else body)

            header = re.sub(r"Content-Length: \d+\n", "", header)

            exec(code, {}, {
                "console": self.console,
                "header": header,
                "body": body,
                "args": {var: None for var in vars}
            })

            self.console.success("Code executed successfully")

        except Exception as e:
            self.console.error(str(e))
        finally:
            self.run_btn.configure(state="normal")

    def toggle_topmost(self):
        """Toggle the topmost property of the window."""
        self.master.attributes("-topmost", self.topmost_switch.get())
        self.console.info(f"Topmost is {'enabled' if self.topmost_switch.get() else 'disabled'}")
