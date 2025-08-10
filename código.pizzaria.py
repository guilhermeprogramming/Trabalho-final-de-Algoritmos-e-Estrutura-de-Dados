# Trabalho final de Algoritmos e Estruturas de Dados - Guilherme Galdino Jacinto
# Tema: Pizzaria com atendimento por fila (FIFO)
#Resumo:
#Fila FIFO → Mantém a ordem de chegada (First In, First Out).
#Inserir e remover são sempre O(1) (constantes).
#A única operação O(n) é atualizar a lista na interface, pois percorremos todos os pedidos para exibir.
import tkinter as tk
from tkinter import messagebox
from collections import deque
# ------------------------
# Sistema da Pizzaria (apenas fila FIFO)
# ------------------------
class SistemaPizzaria:
    def __init__(self):
        self.fila_pedidos = deque()  # fila geral

    def adicionar_pedido(self, pedido):
        self.fila_pedidos.append(pedido)  # O(1)

    def concluir_pedido(self):
        if not self.fila_pedidos:
            return None
        return self.fila_pedidos.popleft()  # O(1)

    def listar_fila(self):
        return list(self.fila_pedidos)  # O(n)
# ------------------------
# Interface Tkinter
# ------------------------
class App:
    def __init__(self, root):
        self.sistema = SistemaPizzaria()
        self.tipo_pedido = tk.StringVar(value="Entrega")  # padrão

        root.title("Sistema de Pedidos - Pizzaria")
        root.geometry("600x500")

        # Tipo de pedido
        tk.Label(root, text="Tipo de Pedido:").pack()
        tk.Radiobutton(root, text="Entrega", variable=self.tipo_pedido, value="Entrega", command=self.atualizar_campos).pack()
        tk.Radiobutton(root, text="Restaurante", variable=self.tipo_pedido, value="Restaurante", command=self.atualizar_campos).pack()

        # Campos para Entrega
        self.label_nome = tk.Label(root, text="Nome do Cliente:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(root, width=40)
        self.entry_nome.pack()

        self.label_endereco = tk.Label(root, text="Endereço:")
        self.label_endereco.pack()
        self.entry_endereco = tk.Entry(root, width=40)
        self.entry_endereco.pack()

        # Campo para Restaurante
        self.label_mesa = tk.Label(root, text="Número da Mesa:")
        self.entry_mesa = tk.Entry(root, width=10)

        # Campos comuns
        tk.Label(root, text="Sabor da Pizza:").pack()
        self.entry_sabor = tk.Entry(root, width=40)
        self.entry_sabor.pack()

        tk.Label(root, text="Tamanho (P, M, G):").pack()
        self.entry_tamanho = tk.Entry(root, width=10)
        self.entry_tamanho.pack()

        # Botões
        tk.Button(root, text="Adicionar Pedido", command=self.adicionar).pack(pady=5)
        tk.Button(root, text="Concluir Próximo Pedido", command=self.concluir).pack(pady=5)

        # Lista de pedidos
        tk.Label(root, text="Fila de Pedidos (ordem de chegada):").pack()
        self.lista_fila = tk.Listbox(root, height=12)
        self.lista_fila.pack(fill="x", padx=10)

        self.atualizar_campos()

    def atualizar_campos(self):
        """Mostra/oculta campos conforme o tipo de pedido"""
        if self.tipo_pedido.get() == "Entrega":
            self.label_nome.pack()
            self.entry_nome.pack()
            self.label_endereco.pack()
            self.entry_endereco.pack()
            self.label_mesa.pack_forget()
            self.entry_mesa.pack_forget()
        else:
            self.label_nome.pack_forget()
            self.entry_nome.pack_forget()
            self.label_endereco.pack_forget()
            self.entry_endereco.pack_forget()
            self.label_mesa.pack()
            self.entry_mesa.pack()

    def atualizar_lista(self):
        """Atualiza Listbox com a fila de pedidos"""
        self.lista_fila.delete(0, tk.END)
        for p in self.sistema.listar_fila():
            if p["tipo"] == "Entrega":
                self.lista_fila.insert(tk.END, f"Entrega: {p['nome']} - {p['sabor']} ({p['tamanho']}) - {p['endereco']}")
            else:
                self.lista_fila.insert(tk.END, f"Mesa {p['mesa']}: {p['sabor']} ({p['tamanho']})")

    def adicionar(self):
        """Adiciona pedido na fila"""
        tipo = self.tipo_pedido.get()
        sabor = self.entry_sabor.get().strip()
        tamanho = self.entry_tamanho.get().strip().upper()

        if not sabor or tamanho not in ["P", "M", "G"]:
            messagebox.showerror("Erro", "Preencha sabor e tamanho corretamente!")
            return

        if tipo == "Entrega":
            nome = self.entry_nome.get().strip()
            endereco = self.entry_endereco.get().strip()
            if not nome or not endereco:
                messagebox.showerror("Erro", "Preencha nome e endereço para entrega!")
                return
            pedido = {"tipo": "Entrega", "nome": nome, "endereco": endereco, "sabor": sabor, "tamanho": tamanho}
        else:
            mesa = self.entry_mesa.get().strip()
            if not mesa.isdigit():
                messagebox.showerror("Erro", "Informe um número de mesa válido!")
                return
            pedido = {"tipo": "Restaurante", "mesa": mesa, "sabor": sabor, "tamanho": tamanho}

        self.sistema.adicionar_pedido(pedido)
        self.limpar_campos()
        self.atualizar_lista()

    def concluir(self):
        """Remove o primeiro pedido da fila"""
        pedido = self.sistema.concluir_pedido()
        if pedido:
            if pedido["tipo"] == "Entrega":
                msg = f"Pedido de entrega concluído: {pedido['nome']} - {pedido['sabor']} ({pedido['tamanho']})"
            else:
                msg = f"Pedido mesa {pedido['mesa']} concluído: {pedido['sabor']} ({pedido['tamanho']})"
            messagebox.showinfo("Pedido Concluído", msg)
        else:
            messagebox.showwarning("Aviso", "Nenhum pedido na fila!")
        self.atualizar_lista()

    def limpar_campos(self):
        """Limpa campos de entrada"""
        self.entry_nome.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_mesa.delete(0, tk.END)
        self.entry_sabor.delete(0, tk.END)
        self.entry_tamanho.delete(0, tk.END)
# ------------------------
# Execução
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
