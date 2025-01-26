from tkinter import filedialog
from PIL import Image
from sympy import *
import customtkinter
from Polynomial import *
import Processing

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class FileNotSelected(customtkinter.CTkToplevel):
    # when file is not selected, executed
    def __init__(self):
        super().__init__()
        self.title("Warning!!")
        self.geometry("300,50")
        self.label_1 = customtkinter.CTkLabel(self, text="Please Select a file!!", text_color="red")
        self.label_1.grid(padx=20, pady=20)
        self.b1 = customtkinter.CTkButton(self, text="OK!", command=self.regainFocus)
        self.b1.grid(padx=20, pady=20)

    def regainFocus(self):
        app.deiconify()
        self.destroy()


class ConfirmImage(customtkinter.CTkToplevel):
    # For file selection confirmation
    def __init__(self, path):
        super().__init__()
        self.geometry("445x340")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        image = customtkinter.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(384, 216))
        self.frame = customtkinter.CTkFrame(self, width=460, height=260)
        self.frame.grid(padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.Label = customtkinter.CTkLabel(self.frame, text="Is This The Correct Image...", corner_radius=0,
                                            compound="bottom", image=image, anchor='s')
        self.Label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.button1 = customtkinter.CTkButton(self.frame, text="YES", command=self.right(path))
        self.button1.grid(row=1, padx=(10, 10), pady=(10, 10), column=0, sticky="nsew")
        self.button2 = customtkinter.CTkButton(self.frame, text="No", command=self.wrong)
        self.button2.grid(row=1, padx=(10, 10), pady=(10, 10), column=1, sticky="nsew")

    def right(self, path):
        self.destroy()
        app.deiconify()
        s = Processing.predication(path)
        eqn = transform(s)
        app.root_textview.insert("0.0", eqn)

    def wrong(self):
        self.destroy()
        app.path_textview.delete("0.0", "end")


class WrongFile(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("500,100")
        self.title("Warning!!")
        self.label_1 = customtkinter.CTkLabel(self, text="You can only input Image!!", text_color="red", width=300)
        self.b1 = customtkinter.CTkButton(self, text="OK!", command=self.regainFocus)
        self.label_1.grid(padx=20, pady=20)
        self.b1.grid(padx=20, pady=20)

    def regainFocus(self):
        app.deiconify()
        self.destroy()


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window and grid setup
        self.title("Polynomial Solver")
        self.geometry(f"{645}x{580}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.toplevel_window = None

        # sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=50, corner_radius=3)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Reset")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.destroy)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"],
                                                                       command=self.appear)
        self.appearance_mode_option_menu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "120%", "150%"],
                                                               command=self.scale)
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # image input frame
        self.logo_label = customtkinter.CTkLabel(self, text="Upload Image..",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), compound="left")
        self.logo_label.grid(row=0, column=1, padx=(10, 280), pady=(10, 0))
        self.image_input_frame = customtkinter.CTkFrame(self)
        self.image_input_frame.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.image_input_frame.grid_columnconfigure(1, weight=1)
        self.path_textview = customtkinter.CTkTextbox(self.image_input_frame, height=50, width=330)
        self.path_textview.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10))
        self.path_input = customtkinter.CTkButton(self.image_input_frame, text="Select", command=self.path)
        self.path_input.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))

        # root finder
        self.root_input_frame = customtkinter.CTkFrame(self)
        self.root_input_frame.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.root_label = customtkinter.CTkLabel(self.root_input_frame, text="Roots",
                                                 font=customtkinter.CTkFont(size=14, weight="bold"), compound="left")
        self.root_label.grid(row=0, column=0, padx=(10, 290), pady=(10, 0))
        self.root_input_frame.grid_columnconfigure(1, weight=1)
        self.root_textview = customtkinter.CTkTextbox(self.root_input_frame, height=30, width=330)
        self.root_textview.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="nsew")
        self.root_tabview = customtkinter.CTkTabview(self.root_input_frame, corner_radius=8)
        self.root_tabview.add("Polynomial")
        self.root_tabview.add("Integration")
        self.root_tabview.add("Differentiation")
        self.root_tabview.grid(row=3, column=0, padx=(20, 20), pady=(10, 20))

        # Polynomial
        self.root_input_1 = customtkinter.CTkButton(self.root_tabview.tab("Polynomial"), text="Solve",
                                                    command=self.poly)
        self.root_input_1.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        self.root_textview_1 = customtkinter.CTkTextbox(self.root_tabview.tab("Polynomial"), height=90, width=330)
        self.root_textview_1.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        self.root_textview_1.configure(state="disabled")

        # Integration
        self.root_input_2 = customtkinter.CTkButton(self.root_tabview.tab("Integration"), text="Solve",
                                                    command=self.int)
        self.root_input_2.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        self.root_textview_2 = customtkinter.CTkTextbox(self.root_tabview.tab("Integration"), height=90, width=330)
        self.root_textview_2.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        self.root_textview_2.configure(state="disabled")

        # Differentiation
        self.root_input = customtkinter.CTkButton(self.root_tabview.tab("Differentiation"), text="Solve",
                                                  command=self.diff)
        self.root_input.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 20))
        self.root_textview_3 = customtkinter.CTkTextbox(self.root_tabview.tab("Differentiation"), height=90, width=330)
        self.root_textview_3.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        self.root_textview_3.configure(state="disabled")

    def poly(self):
        equation = self.root_textview.get("0.0", "end")
        eqn = reverse_transform(equation)
        roots = polynomial(eqn)
        self.root_textview_1.configure(state="normal")
        self.root_textview_1.delete("0.0", "end")
        r=1
        if not roots:
            self.root_textview_1.insert("end", "No roots found for the given equation.")
        else:
            for i, j in roots.items():
                for k in range(0, j):
                    self.root_textview_1.insert("end", f'x{r} = {i} \n\n')
                    r = r+1
            self.root_textview_1.insert("end", "are the roots of the given equation.")
        self.root_textview_1.configure(state="disabled")

    def int(self):
        equation = self.root_textview.get("0.0", "end")
        eqn = reverse_transform(equation)
        try:
            integrate_result = pretty(integration(eqn))
            self.root_textview_2.configure(state="normal")
            self.root_textview_2.delete("0.0", "end")
            self.root_textview_2.insert("end", integrate_result)
        except Exception as e:
            self.root_textview_2.configure(state="normal")
            self.root_textview_2.delete("0.0", "end")
            self.root_textview_2.insert("end", "Error: " + str(e))
        finally:
            self.root_textview_2.configure(state="disabled")

    def diff(self):
        equation = self.root_textview.get("0.0", "end")
        eqn = reverse_transform(equation)
        try:
            diff_result = pretty(differentiate(eqn))
            self.root_textview_3.configure(state="normal")
            self.root_textview_3.delete("0.0", "end")
            self.root_textview_3.insert("end", diff_result)
        except Exception as e:
            self.root_textview_3.configure(state="normal")
            self.root_textview_3.delete("0.0", "end")
            self.root_textview_3.insert("end", "Error: " + str(e))
        finally:
            self.root_textview_3.configure(state="disabled")

    def appear(self, new: str):
        customtkinter.set_appearance_mode(new)

    def scale(self, new: str):
        new_scaling_float = int(new.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def path(self):
        p = filedialog.askopenfilename()
        if len(p) == 0:
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = FileNotSelected()
                self.toplevel_window.focus()
            else:
                self.toplevel_window.destroy()
                self.toplevel_window = FileNotSelected()
                self.toplevel_window.focus()

        else:
            try:
                with Image.open(p) as img:
                    self.path_textview.delete("0.0", "end")
                    self.path_textview.insert("0.0", p)
                    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                        self.toplevel_window = ConfirmImage(p)
                        self.toplevel_window.focus()
                    else:
                        self.toplevel_window.destroy()
                        self.toplevel_window = ConfirmImage(p)
                        self.toplevel_window.focus()

            except IOError:
                if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                    self.toplevel_window = WrongFile()
                    self.toplevel_window.focus()
                    self.withdraw()
                else:
                    self.toplevel_window.destroy()
                    self.toplevel_window = WrongFile()
                    self.toplevel_window.focus()


if __name__ == "__main__":
    app = Gui()
    app.mainloop()
