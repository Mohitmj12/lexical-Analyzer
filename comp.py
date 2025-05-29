import re
import tkinter as tk
from tkinter import scrolledtext

class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter your code:").pack()
        
        self.code_input = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.code_input.pack()
        
        self.language_var = tk.StringVar(value="c")
        tk.Label(self.root, text="Select Language:").pack()
        
        tk.OptionMenu(self.root, self.language_var, "c", "cpp", "java", "python").pack()
        
        tk.Button(self.root, text="Analyze", command=self.analyze_code).pack()
        
        tk.Label(self.root, text="Tokens:").pack()
        self.output_display = scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.output_display.pack()
    
    def analyze_code(self):
        code = self.code_input.get("1.0", tk.END).strip()
        language = self.language_var.get()
        tokens, errors = self.tokenize(code, language)
        
        self.output_display.delete("1.0", tk.END)
        for token in tokens:
            self.output_display.insert(tk.END, f"{token[0]:<15}: {token[1]}\n")
        
        if errors:
            self.output_display.insert(tk.END, "\nErrors:\n" + "\n".join(errors))
    
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
            ('INVALID', r'[^\w\s]')
        ]
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        tokens = []
        errors = []
        for match in re.finditer(token_regex, code, re.DOTALL):
            kind = match.lastgroup
            value = match.group()
            if kind == "INVALID":
                errors.append(f"Invalid token: {value}")
            else:
                tokens.append((kind, value))
        return tokens, errors

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
