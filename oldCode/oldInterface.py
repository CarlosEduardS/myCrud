import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="escola"
    )

def carregar_lista():
    for row in tree.get_children():
        tree.delete(row)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def inserir():
    nome = entry_nome.get().strip()
    idade = entry_idade.get().strip()
    turma = entry_turma.get().strip()

    if not nome or not idade or not turma:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    
    if not idade.isnumeric():
        messagebox.showwarning("Aviso", "Idade deve ser um número!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, idade, turma) VALUES (%s, %s, %s)",
            (nome, int(idade), turma)
        )
        conn.commit()
        conn.close()
        limpar_campos()
        carregar_lista()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def deletar():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno na lista!")
        return
    valores = tree.item(selecionado, "values")
    id_aluno = valores[0]
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
        conn.commit()
        conn.close()
        carregar_lista()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def preencher_campos(event):
    selecionado = tree.focus()
    if not selecionado:
        return
    valores = tree.item(selecionado, "values")
    limpar_campos()
    entry_nome.insert(0, valores[1])
    entry_idade.insert(0, valores[2])
    entry_turma.insert(0, valores[3])

def atualizar():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno na lista!")
        return
    id_aluno = tree.item(selecionado, "values")[0]
    nome = entry_nome.get().strip()
    idade = entry_idade.get().strip()
    turma = entry_turma.get().strip()

    if not nome or not idade or not turma:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if not idade.isnumeric():
        messagebox.showwarning("Aviso", "Idade deve ser um número!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alunos SET nome=%s, idade=%s, turma=%s WHERE id=%s",
            (nome, int(idade), turma, id_aluno)
        )
        conn.commit()
        conn.close()
        limpar_campos()
        carregar_lista()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_turma.delete(0, tk.END)

# --- Interface ---
root = tk.Tk()
root.title("Cadastro de Alunos")
root.geometry("1280x1024")
root.resizable(False, False)

# Formulário
frame_form = tk.LabelFrame(root, text="Dados do Aluno", padx=10, pady=10)
frame_form.pack(fill="x", padx=15, pady=10)

tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=4)
entry_nome = tk.Entry(frame_form, width=25)
entry_nome.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Idade:").grid(row=0, column=2, sticky="e", padx=5)
entry_idade = tk.Entry(frame_form, width=8)
entry_idade.grid(row=0, column=3, padx=5)

tk.Label(frame_form, text="Turma:").grid(row=0, column=4, sticky="e", padx=5)
entry_turma = tk.Entry(frame_form, width=10)
entry_turma.grid(row=0, column=5, padx=5)

# Botões
frame_btn = tk.Frame(root)
frame_btn.pack(pady=5)

tk.Button(frame_btn, text="Inserir",   width=12, bg="#4CAF50", fg="white", command=inserir).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Atualizar", width=12, bg="#2196F3", fg="white", command=atualizar).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Deletar",   width=12, bg="#f44336", fg="white", command=deletar).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Limpar",    width=12, command=limpar_campos).grid(row=0, column=3, padx=5)

# Tabela
frame_tree = tk.LabelFrame(root, text="Alunos Cadastrados", padx=10, pady=5)
frame_tree.pack(fill="both", expand=True, padx=15, pady=10)

colunas = ("id", "nome", "idade", "turma")
tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=10)
tree.heading("id",    text="ID")
tree.heading("nome",  text="Nome")
tree.heading("idade", text="Idade")
tree.heading("turma", text="Turma")
tree.column("id",    width=40,  anchor="center")
tree.column("nome",  width=220)
tree.column("idade", width=60,  anchor="center")
tree.column("turma", width=100, anchor="center")
tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", preencher_campos)

carregar_lista()
root.mainloop()