import customtkinter as ctk

from app import colors


class Console(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        # ============ create widgets ============
        self.text_box = ctk.CTkTextbox(master=self,
                                       corner_radius=0,
                                       fg_color=colors.content1,
                                       font=("Roboto Mono", 10),
                                       wrap="word",
                                       width=220,
                                       padx=5, pady=5,
                                       state="disabled")

        # ============ configure widgets ============
        self.text_box.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text_box.pack(fill="both", expand=True)

        for code in colors:
            self.text_box.tag_config(code, foreground=colors.to_dict()[code])

    def log(self, msg, color="$grey", end="\n") -> None:
        self.text_box.configure(state="normal")

        color_dict = colors.to_dict()

        i = 0
        while i < len(msg):
            for color_code in color_dict:
                if msg[i:].startswith(color_code):
                    color = color_code
                    i += len(color_code)
                    break
            self.text_box.insert("end", msg[i], color)
            i += 1
        self.text_box.insert("end", end)
        self.text_box.yview("moveto", 1)
        self.text_box.configure(state="disabled")

    def info(self, msg="Info") -> None:
        self.log("$blue[*] $white" + msg)

    def success(self, msg="Done") -> None:
        self.log("$green[+] $white" + msg)

    def warning(self, msg="Warning", end="\n") -> None:
        self.log("$orange[!] $white" + msg, end=end)

    def error(self, msg="Error") -> None:
        self.log("$red[-] $white" + msg)

    def draw_line(self, char="~", count=32) -> None:
        self.log(char * count, "$content4", end="\n")
