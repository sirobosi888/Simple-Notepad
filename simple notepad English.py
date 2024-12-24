import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font as tkfont

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()

        # Application settings
        self.title("Notepad")
        self.geometry("600x400")

        # Create text widget
        self.text_area = tk.Text(self, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Create menu
        self.create_menu()

        # Initial file path
        self.current_file = None

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_command(label="Change Font", command=self.change_font)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Search menu
        search_menu = tk.Menu(menu_bar, tearoff=0)
        search_menu.add_command(label="Search", command=self.search_text)
        search_menu.add_command(label="Reset Highlight", command=self.reset_highlight)
        menu_bar.add_cascade(label="Search", menu=search_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Set the menu bar
        self.config(menu=menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.title("Notepad - New")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.current_file = file_path
                    self.title(f"Notepad - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open the file: {e}")

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if not file_path:
                return
        else:
            file_path = self.current_file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content.strip())
                self.current_file = file_path
                self.title(f"Notepad - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file: {e}")

    def undo(self):
        try:
            self.text_area.edit_undo()
        except Exception as e:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except Exception as e:
            pass

    def change_font(self):
        # Font change dialog
        font_choice = simpledialog.askstring("Change Font", "Enter the new font name (e.g., Arial, Courier, etc.):")
        size_choice = simpledialog.askinteger("Change Font Size", "Enter the font size (e.g., 12, 14, etc.):")

        if font_choice and size_choice:
            try:
                new_font = tkfont.Font(family=font_choice, size=size_choice)
                self.text_area.config(font=new_font)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change font: {e}")

    def search_text(self):
        # Show search bar
        search_term = simpledialog.askstring("Search", "Enter the word to search for:")
        if search_term:
            self.highlight_text(search_term)

    def highlight_text(self, word):
        # Highlight a specific word
        self.reset_highlight()
        start_pos = "1.0"
        while True:
            start_pos = self.text_area.search(word, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(word)}c"
            self.text_area.tag_add("highlight", start_pos, end_pos)
            self.text_area.tag_configure("highlight", background="yellow")
            start_pos = end_pos

    def reset_highlight(self):
        # Reset highlight
        self.text_area.tag_remove("highlight", "1.0", tk.END)

    def show_help(self):
        # Show help dialog in English
        messagebox.showinfo("Help", "How to use the Notepad:\n1. New file: 'New' button\n2. Open file: 'Open' button\n3. Save file: 'Save' button\n4. Change font: 'Edit' -> 'Change Font'\n5. Search: 'Search' -> 'Search' button\n6. Reset highlight: 'Search' -> 'Reset Highlight' button\n\nVersion 1.0")

if __name__ == "__main__":
    # Run the application
    app = Notepad()
    app.mainloop()
