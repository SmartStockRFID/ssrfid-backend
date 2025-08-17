import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:8000/pecas"
LOGIN_URL = "http://localhost:8000/login"
USUARIOS_URL = "http://localhost:8000/usuarios"

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Estoque Toyota Newland")
        self.root.geometry("900x500")
        self.token = None
        self.user_role = None
        self.show_login()

    def show_login(self):
        self.login_win = tk.Toplevel(self.root)
        self.login_win.title("Login - Admin")
        self.login_win.geometry("300x200")
        self.login_win.grab_set()
        tk.Label(self.login_win, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_win)
        self.username_entry.pack(pady=5)
        tk.Label(self.login_win, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_win, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.login_win, text="Entrar", command=self.login).pack(pady=10)
        self.login_win.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            resp = requests.post(LOGIN_URL, data={"username": username, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                
                # Abordagem alternativa: usar o username para determinar o role
                # Se for 'admin', assume role de administrador
                if username == "admin":
                    self.user_role = "admin"
                else:
                    # Para outros usuários, assume role padrão
                    self.user_role = "user"
                
                self.login_win.destroy()
                self.search_var = tk.StringVar()
                self.create_widgets()
                self.load_pecas()
            else:
                messagebox.showerror("Erro de login", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar: {e}")

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Buscar por nome:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Buscar", command=self.buscar_pecas).pack(side=tk.LEFT)
        tk.Button(frame, text="Atualizar", command=self.load_pecas).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "codigo_oem", "modelo_carro", "ano_carro", "quantidade"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(expand=True, fill=tk.BOTH, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Adicionar", command=self.adicionar_peca).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Editar", command=self.editar_peca).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Deletar", command=self.deletar_peca).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Voltar", command=self.voltar_busca).pack(side=tk.LEFT, padx=5)
        
        # Botão para criar usuário (apenas para admins)
        if self.user_role == "admin":
            tk.Button(btn_frame, text="Criar Usuário", command=self.criar_usuario, 
                     bg="#4CAF50", fg="white", relief=tk.RAISED).pack(side=tk.LEFT, padx=5)

    def voltar_busca(self):
        self.search_var.set("")
        self.load_pecas()

    def load_pecas(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            resp = requests.get(API_URL, headers=headers)
            resp.raise_for_status()
            pecas = resp.json()
            self.tree.delete(*self.tree.get_children())
            for p in pecas:
                self.tree.insert("", "end", values=(p["id"], p["nome"], p["codigo_oem"], p["modelo_carro"], p["ano_carro"], p["quantidade"]))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar peças: {e}")

    def buscar_pecas(self):
        nome = self.search_var.get()
        if len(nome) < 3:
            messagebox.showwarning("Atenção", "Digite pelo menos 3 caracteres para buscar.")
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            resp = requests.get(f"{API_URL}/busca", params={"nome": nome}, headers=headers)
            resp.raise_for_status()
            pecas = resp.json()
            self.tree.delete(*self.tree.get_children())
            for p in pecas:
                self.tree.insert("", "end", values=(p["id"], p["nome"], p["codigo_oem"], p["modelo_carro"], p["ano_carro"], p["quantidade"]))
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                messagebox.showinfo("Busca", "Nenhuma peça encontrada.")
            else:
                messagebox.showerror("Erro", f"Erro na busca: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar peças: {e}")

    def adicionar_peca(self):
        self.peca_form("Adicionar Peça")

    def editar_peca(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma peça para editar.")
            return
        peca_id = self.tree.item(item[0])["values"][0]
        self.peca_form("Editar Peça", peca_id)

    def deletar_peca(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma peça para deletar.")
            return
        peca_id = self.tree.item(item[0])["values"][0]
        if messagebox.askyesno("Confirmação", "Deseja realmente deletar esta peça?"):
            try:
                headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
                resp = requests.delete(f"{API_URL}/{peca_id}", headers=headers)
                resp.raise_for_status()
                self.load_pecas()
                messagebox.showinfo("Sucesso", "Peça deletada com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao deletar peça: {e}")

    def peca_form(self, title, peca_id=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("400x400")
        campos = ["nome", "codigo_oem", "descricao", "localizacao", "quantidade", "preco_custo", "preco_venda", "modelo_carro", "ano_carro"]
        entries = {}
        for i, campo in enumerate(campos):
            tk.Label(form, text=campo).grid(row=i, column=0, sticky=tk.W, pady=2)
            entries[campo] = tk.Entry(form, width=30)
            entries[campo].grid(row=i, column=1, pady=2)
        if peca_id:
            try:
                headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
                resp = requests.get(f"{API_URL}/{peca_id}", headers=headers)
                resp.raise_for_status()
                peca = resp.json()
                for campo in campos:
                    entries[campo].insert(0, peca[campo])
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar peça: {e}")
        def salvar():
            dados = {campo: entries[campo].get() for campo in campos}
            try:
                headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
                if peca_id:
                    resp = requests.put(f"{API_URL}/{peca_id}", json=dados, headers=headers)
                else:
                    resp = requests.post(API_URL, json=dados, headers=headers)
                resp.raise_for_status()
                self.load_pecas()
                messagebox.showinfo("Sucesso", "Peça salva com sucesso.")
                form.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar peça: {e}")
        tk.Button(form, text="Salvar", command=salvar).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def criar_usuario(self):
        """Abre formulário para criação de novo usuário"""
        if self.user_role != "admin":
            messagebox.showerror("Acesso Negado", "Apenas administradores podem criar usuários.")
            return
            
        self.usuario_form("Criar Novo Usuário")

    def usuario_form(self, title):
        """Formulário para criação de usuário"""
        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("350x250")
        form.grab_set()  # Torna o formulário modal
        
        # Centralizar o formulário
        form.transient(self.root)
        form.grab_set()
        
        # Frame principal com padding
        main_frame = tk.Frame(form, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos do formulário
        campos = [
            ("username", "Nome de Usuário:"),
            ("password", "Senha:"),
            ("confirm_password", "Confirmar Senha:"),
            ("role", "Papel:")
        ]
        
        entries = {}
        for i, (campo, label) in enumerate(campos):
            tk.Label(main_frame, text=label, anchor=tk.W).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if campo == "password" or campo == "confirm_password":
                entries[campo] = tk.Entry(main_frame, width=25, show="*")
            elif campo == "role":
                # Combobox para seleção de papel
                entries[campo] = ttk.Combobox(main_frame, width=22, 
                                            values=["estoquista", "admin", "vendedor"], 
                                            state="readonly")
                entries[campo].set("estoquista")  # Valor padrão
            else:
                entries[campo] = tk.Entry(main_frame, width=25)
            
            entries[campo].grid(row=i, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Frame para botões
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        def salvar_usuario():
            """Valida e salva o novo usuário"""
            # Validação dos campos
            username = entries["username"].get().strip()
            password = entries["password"].get()
            confirm_password = entries["confirm_password"].get()
            role = entries["role"].get()
            
            # Validações
            if not username:
                messagebox.showerror("Erro", "Nome de usuário é obrigatório.")
                return
                
            if len(username) < 3:
                messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 3 caracteres.")
                return
                
            if not password:
                messagebox.showerror("Erro", "Senha é obrigatória.")
                return
                
            if len(password) < 6:
                messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres.")
                return
                
            if password != confirm_password:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return
                
            if not role:
                messagebox.showerror("Erro", "Papel é obrigatório.")
                return
            
            # Dados para envio
            dados = {
                "username": username,
                "password": password,
                "role": role
            }
            
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                resp = requests.post(USUARIOS_URL, json=dados, headers=headers)
                
                if resp.status_code == 201:
                    messagebox.showinfo("Sucesso", f"Usuário '{username}' criado com sucesso!")
                    form.destroy()
                elif resp.status_code == 400:
                    error_data = resp.json()
                    if "Usuário já existe" in error_data.get("detail", ""):
                        messagebox.showerror("Erro", f"Usuário '{username}' já existe no sistema.")
                    else:
                        messagebox.showerror("Erro", f"Erro na criação: {error_data.get('detail', 'Erro desconhecido')}")
                elif resp.status_code == 403:
                    messagebox.showerror("Erro", "Acesso negado. Apenas administradores podem criar usuários.")
                else:
                    messagebox.showerror("Erro", f"Erro na criação: {resp.status_code}")
                    
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Erro", "Falha na conexão com o servidor.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {e}")
        
        def cancelar():
            """Fecha o formulário sem salvar"""
            form.destroy()
        
        # Botões
        tk.Button(btn_frame, text="Salvar", command=salvar_usuario, 
                 bg="#4CAF50", fg="white", relief=tk.RAISED, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancelar", command=cancelar, 
                 bg="#f44336", fg="white", relief=tk.RAISED, width=10).pack(side=tk.LEFT, padx=5)
        
        # Focar no primeiro campo
        entries["username"].focus()
        
        # Bind Enter para salvar
        form.bind('<Return>', lambda e: salvar_usuario())
        form.bind('<Escape>', lambda e: cancelar())

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
