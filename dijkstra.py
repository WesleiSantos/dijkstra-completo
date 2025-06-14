import heapq
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')  # Definindo o backend adequado para o Tkinter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador e Analisador de Grafos")
        
        # Variáveis de controle
        self.tipo_entrada = tk.IntVar(value=1)
        self.grafo = None
        self.num_vertices = 0
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção de seleção de tipo de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Tipo de Entrada", padding="10")
        entrada_frame.pack(fill=tk.X, pady=5)
        
        # Opções de entrada
        ttk.Radiobutton(entrada_frame, text="1. Arquivo TXT", variable=self.tipo_entrada, 
                        value=1, command=self.mostrar_opcoes).pack(anchor=tk.W)
        ttk.Radiobutton(entrada_frame, text="2. Grau X para todos os nós", variable=self.tipo_entrada, 
                        value=2, command=self.mostrar_opcoes).pack(anchor=tk.W)
        ttk.Radiobutton(entrada_frame, text="3. Grau X para Y nós e intervalo para os demais", 
                        variable=self.tipo_entrada, value=3, command=self.mostrar_opcoes).pack(anchor=tk.W)
        
        # Frame para opções específicas
        self.opcoes_frame = ttk.Frame(main_frame)
        self.opcoes_frame.pack(fill=tk.X, pady=5)
        
        # Frame para resultados e ações
        acoes_frame = ttk.LabelFrame(main_frame, text="Ações", padding="10")
        acoes_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botões de ação
        ttk.Button(acoes_frame, text="Gerar Grafo", command=self.gerar_grafo).pack(side=tk.LEFT, padx=5)
        ttk.Button(acoes_frame, text="Mostrar Topologia", command=self.mostrar_topologia).pack(side=tk.LEFT, padx=5)
        ttk.Button(acoes_frame, text="Calcular Caminhos", command=self.calcular_caminhos).pack(side=tk.LEFT, padx=5)
        ttk.Button(acoes_frame, text="Salvar Resultados", command=self.salvar_resultados).pack(side=tk.LEFT, padx=5)
        
        # Mostrar opções iniciais
        self.mostrar_opcoes()
    
    def mostrar_opcoes(self):
        # Limpar frame de opções
        for widget in self.opcoes_frame.winfo_children():
            widget.destroy()
        
        tipo = self.tipo_entrada.get()
        
        if tipo == 1:  # Arquivo TXT
            ttk.Label(self.opcoes_frame, text="Caminho do arquivo:").pack(side=tk.LEFT)
            self.arquivo_entry = ttk.Entry(self.opcoes_frame, width=40)
            self.arquivo_entry.pack(side=tk.LEFT, padx=5)
            ttk.Button(self.opcoes_frame, text="Procurar", command=self.procurar_arquivo).pack(side=tk.LEFT)
        
        elif tipo == 2:  # Grau X para todos
            ttk.Label(self.opcoes_frame, text="Número de nós:").pack(side=tk.LEFT)
            self.n_nos_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.n_nos_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.opcoes_frame, text="Grau desejado:").pack(side=tk.LEFT)
            self.grau_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.grau_entry.pack(side=tk.LEFT, padx=5)
        
        elif tipo == 3:  # Grau X para Y nós e intervalo
            ttk.Label(self.opcoes_frame, text="Número total de nós:").pack(side=tk.LEFT)
            self.n_total_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.n_total_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.opcoes_frame, text="Número de nós com grau fixo:").pack(side=tk.LEFT)
            self.n_fixo_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.n_fixo_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.opcoes_frame, text="Grau fixo:").pack(side=tk.LEFT)
            self.grau_fixo_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.grau_fixo_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.opcoes_frame, text="Grau mínimo para outros:").pack(side=tk.LEFT)
            self.grau_min_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.grau_min_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.opcoes_frame, text="Grau máximo para outros:").pack(side=tk.LEFT)
            self.grau_max_entry = ttk.Entry(self.opcoes_frame, width=5)
            self.grau_max_entry.pack(side=tk.LEFT, padx=5)
    
    def procurar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
        if caminho:
            self.arquivo_entry.delete(0, tk.END)
            self.arquivo_entry.insert(0, caminho)
    
    def ler_grafo_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r') as f:
                linhas = f.readlines()

            num_vertices = int(linhas[0])
            grafo = {i: [] for i in range(1, num_vertices + 1)}

            for linha in linhas[2:]:
                origem, destino, peso = map(int, linha.strip().split())
                grafo[origem].append((destino, peso))
                grafo[destino].append((origem, peso))  # Adiciona a aresta no sentido inverso

            return grafo, num_vertices
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler arquivo: {str(e)}")
            return None, 0

    def gerar_grafo_regular(self, n_nos, grau):
        # Verifica se é possível criar um grafo regular
        if n_nos <= grau:
            messagebox.showwarning("Aviso", f"Grau deve ser menor que número de nós. Ajustando para {n_nos-1}")
            grau = n_nos - 1

        # Calcula a soma total de graus necessária
        soma_graus = n_nos * grau

        # Se a soma for ímpar, adiciona um grau extra a um nó
        if soma_graus % 2 != 0:
            graus = [grau + 1] + [grau] * (n_nos + 1)
            messagebox.showinfo("Info", f"Ajustando: um nó terá grau {grau+1} (os demais {grau})")
        else:
            graus = [grau] * n_nos

        # Criar grafo usando o modelo de configuração
        grafo = {i: [] for i in range(1, n_nos + 1)}

        # Lista de stubs (arestas pendentes)
        stubs = []
        for i, node in enumerate(range(1, n_nos + 1)):
            stubs.extend([node] * graus[i])

        # Tentativas de conexão
        max_tentativas = 1000
        tentativas = 0

        while len(stubs) > 0 and tentativas < max_tentativas:
            random.shuffle(stubs)
            a = stubs.pop()
            b = stubs.pop()

            # Evitar auto-conexões e arestas duplicadas
            if a != b and not any(v == b for v, _ in grafo[a]):
                peso = random.randint(1, 10)
                grafo[a].append((b, peso))
                grafo[b].append((a, peso))
                tentativas = 0  # Resetar contador se conseguir conectar
            else:
                # Se não puder conectar, recolocar os stubs
                stubs.extend([a, b])
                tentativas += 1

        # Verificação final
        graus_resultantes = {no: len(vizinhos) for no, vizinhos in grafo.items()}
        print("Graus resultantes:", graus_resultantes)

        return grafo, n_nos


    def gerar_grafo_misto(self, n_total, n_fixo, grau_fixo, grau_min, grau_max):
        # Verificar parâmetros
        if n_fixo > n_total:
            messagebox.showerror("Erro", "Número de nós com grau fixo não pode ser maior que o total")
            return None, 0
        
        if grau_min > grau_max:
            messagebox.showerror("Erro", "Grau mínimo não pode ser maior que grau máximo")
            return None, 0
        
        if grau_fixo >= n_total or grau_max >= n_total:
            messagebox.showerror("Erro", "Grau não pode ser maior ou igual ao número de nós")
            return None, 0
        
        # Criar lista de graus
        graus = [grau_fixo] * n_fixo
        graus.extend([random.randint(grau_min, grau_max) for _ in range(n_total - n_fixo)])
        
        # Verificar se a soma é par
        if sum(graus) % 2 != 0:
            # Ajustar um dos graus para tornar a soma par
            graus[-1] += 1
            if graus[-1] > grau_max:
                graus[-1] -= 2
        
        # Criar grafo usando o modelo de configuração
        grafo = {i: [] for i in range(1, n_total + 1)}
        
        # Lista de stubs (arestas pendentes)
        stubs = []
        for i, node in enumerate(range(1, n_total + 1)):
            stubs.extend([node] * graus[i])
        
        random.shuffle(stubs)
        
        while len(stubs) > 0:
            a = stubs.pop()
            b = stubs.pop()
            
            # Evitar auto-conexões e arestas duplicadas
            if a != b and not any(v == b for v, _ in grafo[a]):
                peso = random.randint(1, 10)  # Peso aleatório entre 1 e 10
                grafo[a].append((b, peso))
                grafo[b].append((a, peso))
            else:
                # Se não puder conectar, recolocar os stubs e tentar novamente
                stubs.extend([a, b])
                random.shuffle(stubs)
                
                # Proteção contra loops infinitos
                if len(stubs) > sum(graus):
                    # Não conseguimos completar o grafo, então ajustamos
                    # Conectamos a um nó aleatório que não cause conflito
                    for node in range(1, n_total + 1):
                        if node != a and not any(v == node for v, _ in grafo[a]):
                            peso = random.randint(1, 10)
                            grafo[a].append((node, peso))
                            grafo[node].append((a, peso))
                            break
                    break
        
        return grafo, n_total
    
    def gerar_grafo(self):
        tipo = self.tipo_entrada.get()
        
        try:
            if tipo == 1:  # Arquivo TXT
                caminho = self.arquivo_entry.get()
                if not caminho:
                    messagebox.showerror("Erro", "Por favor, selecione um arquivo")
                    return
                
                self.grafo, self.num_vertices = self.ler_grafo_arquivo(caminho)
            
            elif tipo == 2:  # Grau X para todos
                n_nos = int(self.n_nos_entry.get())
                grau = int(self.grau_entry.get())
                
                if grau >= n_nos:
                    messagebox.showerror("Erro", "O grau deve ser menor que o número de nós")
                    return
                
                self.grafo, self.num_vertices = self.gerar_grafo_regular(n_nos, grau)
            
            elif tipo == 3:  # Grau X para Y nós e intervalo
                n_total = int(self.n_total_entry.get())
                n_fixo = int(self.n_fixo_entry.get())
                grau_fixo = int(self.grau_fixo_entry.get())
                grau_min = int(self.grau_min_entry.get())
                grau_max = int(self.grau_max_entry.get())
                
                if n_fixo > n_total:
                    messagebox.showerror("Erro", "Número de nós com grau fixo não pode ser maior que o total")
                    return
                
                if grau_min > grau_max:
                    messagebox.showerror("Erro", "Grau mínimo não pode ser maior que grau máximo")
                    return
                
                if grau_fixo >= n_total or grau_max >= n_total:
                    messagebox.showerror("Erro", "Grau não pode ser maior ou igual ao número de nós")
                    return
                
                self.grafo, self.num_vertices = self.gerar_grafo_misto(n_total, n_fixo, grau_fixo, grau_min, grau_max)
            
            if self.grafo:
                messagebox.showinfo("Sucesso", f"Grafo gerado com {self.num_vertices} nós")
        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    
    def mostrar_topologia(self):
        if not self.grafo:
            messagebox.showerror("Erro", "Nenhum grafo foi gerado ainda")
            return
        
        G = nx.Graph()
        for origem, vizinhos in self.grafo.items():
            for destino, peso in vizinhos:
                if not G.has_edge(origem, destino):  # Evita duplicação
                    G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        # Criar uma nova figura
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
                node_size=800, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                   font_color='blue', font_size=8)
        plt.title("Topologia da Rede")
        
        # Configurar a janela do gráfico
        plt.get_current_fig_manager().window.wm_geometry("+%d+%d" % (100, 100))
        plt.tight_layout()
        plt.show()
    
    def dijkstra(self, origem):
        dist = {v: float('inf') for v in self.grafo}
        anterior = {v: None for v in self.grafo}
        dist[origem] = 0
        heap = [(0, origem)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for vizinho, peso in self.grafo[u]:
                if dist[vizinho] > d + peso:
                    dist[vizinho] = d + peso
                    anterior[vizinho] = u
                    heapq.heappush(heap, (dist[vizinho], vizinho))

        return dist, anterior
    
    def reconstruir_caminho(self, anterior, destino):
        caminho = []
        while destino is not None:
            caminho.append(destino)
            destino = anterior[destino]
        return list(reversed(caminho))
    
    def calcular_caminhos(self):
        if not self.grafo:
            messagebox.showerror("Erro", "Nenhum grafo foi gerado ainda")
            return
        
        resultados = []
        distancias = []
        
        for origem in range(1, self.num_vertices + 1):
            dist, anterior = self.dijkstra(origem)
            for destino in range(1, self.num_vertices + 1):
                if origem != destino and dist[destino] != float('inf'):
                    caminho = self.reconstruir_caminho(anterior, destino)
                    resultados.append((f"{origem}-{destino}", '-'.join(map(str, caminho)), dist[destino]))
                    distancias.append(dist[destino])
        
        if not resultados:
            messagebox.showinfo("Resultado", "Não há caminhos entre os nós")
            return
        
        # Encontrar caminho mais curto e mais longo
        caminho_mais_curto = min(resultados, key=lambda x: x[2])
        caminho_mais_longo = max(resultados, key=lambda x: x[2])
        media_distancias = sum(distancias) / len(distancias)
        
        # Mostrar resultados
        resultado_window = tk.Toplevel(self.root)
        resultado_window.title("Resultados dos Caminhos")
        
        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(resultado_window, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(stats_frame, text=f"Caminho mais curto: {caminho_mais_curto[0]} (Distância: {caminho_mais_curto[2]})").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Rota: {caminho_mais_curto[1]}").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Caminho mais longo: {caminho_mais_longo[0]} (Distância: {caminho_mais_longo[2]})").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Rota: {caminho_mais_longo[1]}").pack(anchor=tk.W)
        ttk.Label(stats_frame, text=f"Média das distâncias: {media_distancias:.2f}").pack(anchor=tk.W)
        
        # Frame para tabela de resultados
        table_frame = ttk.Frame(resultado_window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para mostrar os resultados
        tree = ttk.Treeview(table_frame, columns=("Origem/Destino", "Caminho", "Distância"), show="headings")
        tree.heading("Origem/Destino", text="Origem/Destino")
        tree.heading("Caminho", text="Caminho")
        tree.heading("Distância", text="Distância")
        
        for res in resultados:
            tree.insert("", tk.END, values=res)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para salvar
        ttk.Button(resultado_window, text="Salvar Resultados", 
                 command=lambda: self.salvar_resultados_janela(resultados)).pack(pady=5)
    
    def salvar_resultados(self):
        if not self.grafo:
            messagebox.showerror("Erro", "Nenhum grafo foi gerado ainda")
            return
        
        resultados = []
        for origem in range(1, self.num_vertices + 1):
            dist, anterior = self.dijkstra(origem)
            for destino in range(1, self.num_vertices + 1):
                if origem != destino and dist[destino] != float('inf'):
                    caminho = self.reconstruir_caminho(anterior, destino)
                    resultados.append((f"{origem}-{destino}", '-'.join(map(str, caminho)), dist[destino]))
        
        self.salvar_resultados_janela(resultados)
    
    def salvar_resultados_janela(self, resultados):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", 
                                              filetypes=[("Arquivos de texto", "*.txt")])
        if caminho:
            try:
                with open(caminho, 'w') as f:
                    f.write("ORIGEM/DESTINO\t\tCAMINHO\t\tDISTÂNCIA\n")
                    for origem_destino, caminho, distancia in resultados:
                        f.write(f"{origem_destino:<16}\t{caminho:<12}\t{distancia}\n")
                messagebox.showinfo("Sucesso", "Resultados salvos com sucesso")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar arquivo: {str(e)}")

# Executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()