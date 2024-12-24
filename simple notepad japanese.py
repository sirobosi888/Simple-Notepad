import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font as tkfont
import re

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()

        # アプリケーションの設定
        self.title("メモ帳")
        self.geometry("600x400")

        # テキストウィジェットの作成
        self.text_area = tk.Text(self, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # メニューの作成
        self.create_menu()

        # 初期ファイルパス
        self.current_file = None

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # ファイルメニュー
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="新規", command=self.new_file)
        file_menu.add_command(label="開く", command=self.open_file)
        file_menu.add_command(label="保存", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)
        menu_bar.add_cascade(label="ファイル", menu=file_menu)

        # 編集メニュー
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="元に戻す", command=self.undo)
        edit_menu.add_command(label="やり直し", command=self.redo)
        edit_menu.add_command(label="フォント変更", command=self.change_font)
        menu_bar.add_cascade(label="編集", menu=edit_menu)

        # 検索メニュー
        search_menu = tk.Menu(menu_bar, tearoff=0)
        search_menu.add_command(label="検索", command=self.search_text)
        search_menu.add_command(label="ハイライトリセット", command=self.reset_highlight)
        menu_bar.add_cascade(label="検索", menu=search_menu)

        # ヘルプメニュー
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="ヘルプ", command=self.show_help)
        menu_bar.add_cascade(label="ヘルプ", menu=help_menu)
        

        # メニューバーの設定
        self.config(menu=menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.title("メモ帳 - 新規")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.current_file = file_path
                    self.title(f"メモ帳 - {file_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"ファイルを開けませんでした: {e}")

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")])
            if not file_path:
                return
        else:
            file_path = self.current_file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content.strip())
                self.current_file = file_path
                self.title(f"メモ帳 - {file_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを保存できませんでした: {e}")

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
        # フォント変更ダイアログ
        font_choice = simpledialog.askstring("フォント変更", "新しいフォント名を入力（例：Arial, Courier, etc.）:")
        size_choice = simpledialog.askinteger("フォントサイズ変更", "フォントサイズを入力（例：12, 14, etc.）:")

        if font_choice and size_choice:
            try:
                new_font = tkfont.Font(family=font_choice, size=size_choice)
                self.text_area.config(font=new_font)
            except Exception as e:
                messagebox.showerror("エラー", f"フォント変更に失敗しました: {e}")

    def search_text(self):
        # 検索バーを表示
        search_term = simpledialog.askstring("検索", "検索するワードを入力:")
        if search_term:
            self.highlight_text(search_term)

    def highlight_text(self, word):
        # 特定のワードをハイライトする
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
        # ハイライトをリセット
        self.text_area.tag_remove("highlight", "1.0", tk.END)
    def show_help(self):
    # ヘルプダイアログを表示（日本語）
        messagebox.showinfo("ヘルプ", "メモ帳の使い方:\n1. 新規作成: '新規'ボタン\n2. ファイルを開く: '開く'ボタン\n3. ファイルを保存: '保存'ボタン\n4. フォント変更: '編集' -> 'フォント変更'\n5. 検索: '検索' -> '検索'ボタン\n6. ハイライトリセット: '検索' -> 'ハイライトリセット'ボタン \n\nvar 1.0 ")

if __name__ == "__main__":
    # アプリケーションの実行
    app = Notepad()
    app.mainloop()
