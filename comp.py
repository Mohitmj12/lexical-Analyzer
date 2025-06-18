import re
import csv
import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, messagebox

class LexicalAnalyzerGUI:
    def __init__(self, root):  # Corrected from _init_
        self.root = root
        self.root.title("Lexical Analyzer")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter your code:").pack()
        self.code_input = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.code_input.pack()

        self.language_var = tk.StringVar(value="c")
        tk.Label(self.root, text="Select Language:").pack()
        tk.OptionMenu(self.root, self.language_var, "c", "cpp", "java", "python").pack()

        tk.Button(self.root, text="Analyze", command=self.analyze_code).pack(pady=2)
        tk.Button(self.root, text="Save Code", command=self.save_code).pack(pady=2)
        tk.Button(self.root, text="Load Code", command=self.load_code).pack(pady=2)
        tk.Button(self.root, text="Export Tokens to CSV", command=self.export_to_csv).pack(pady=2)
        tk.Button(self.root, text="About", command=self.show_about).pack(pady=2)

        self.token_table = ttk.Treeview(self.root, columns=("Type", "Value", "Line", "Pos"), show="headings")
        for col in ("Type", "Value", "Line", "Pos"):
            self.token_table.heading(col, text=col)
            self.token_table.column(col, width=100)
        self.token_table.pack(fill=tk.BOTH, expand=True)

    def analyze_code(self):
        self.token_table.delete(*self.token_table.get_children())
        code = self.code_input.get("1.0", tk.END)
        language = self.language_var.get()
        tokens, errors = self.tokenize(code, language)
        for token in tokens:
            self.token_table.insert("", tk.END, values=token)
        if errors:
            messagebox.showwarning("Lexical Errors", "\n".join(errors))

    def save_code(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as file:
                file.write(self.code_input.get("1.0", tk.END))

    def load_code(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r") as file:
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, file.read())

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Value", "Line", "Pos"])
                for row in self.token_table.get_children():
                    writer.writerow(self.token_table.item(row)['values'])

    def show_about(self):
        messagebox.showinfo("About Lexical Analyzer", "This tool tokenizes code and displays keywords, identifiers, numbers, operators, etc., with line and column tracking.")

    def tokenize(self, code, language):
        keywords = {
            "c": {"int", "float", "return", "if", "else", "while", "for", "char", "void", "include"},
            "cpp": {"int", "float", "return", "if", "else", "while", "for", "char", "void", "include", "namespace", "std"},
            "java": {"int", "float", "return", "if", "else", "while", "for", "char", "void", "import", "public", "private", "class", "static", "new"},
            "python": {"def", "return", "if", "else", "while", "for", "import", "class", "print"}
        }

        token_specification = [
            ('KEYWORD', r'\b(?:' + '|'.join(keywords[language]) + r')\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
            ('OPERATOR', r'[+\-*/=<>!]+'),
            ('STRING', r'".*?"|\'.*?\''),
            ('COMMENT', r'//.*|#.*'),
            ('MULTILINE_COMMENT', r'/\*.*?\*/'),
            ('SEPARATOR', r'[(){};,]'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n')
        ]

        token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
        tokens = []
        errors = []

        lines = code.split('\n')
        for line_num, line in enumerate(lines, start=1):
            for match in re.finditer(token_regex, line):
                kind = match.lastgroup
                value = match.group()
                col = match.start() + 1
                if kind in ('WHITESPACE', 'NEWLINE'):
                    continue
                tokens.append((kind, value, line_num, col))
        return tokens, errors

if __name__ == "__main__":  # Corrected main check
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
