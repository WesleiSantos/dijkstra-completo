# 📊 Gerador e Analisador de Grafos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicação gráfica para geração, visualização e análise de grafos bidirecionais com pesos.

## 🚀 Recursos Principais

### 🔧 Métodos de Geração
- **Arquivo TXT**: Carrega estrutura do grafo a partir de arquivo
- **Grau Uniforme**: Gera grafo com mesmo grau para todos os nós
- **Grau Misto**: Configura graus específicos para subconjuntos de nós

### 📈 Análises
- Algoritmo de Dijkstra para caminhos mínimos
- Identificação de caminhos mais longos
- Cálculo de média de distâncias
- Visualização interativa da topologia

## 🛠️ Instalação

```bash
git clone https://github.com/WesleiSantos/dijkstra-completo.git
cd dijkstra-completo
pip install -r requirements.txt
```

## USO

```bash
pyhton3 dijkistra.py
```

## Tecnologias

- Python 3.8+
- Matplotlib (visualização)
- NetworkX (manipulação de grafos)
- Tkinter (interface gráfica)
