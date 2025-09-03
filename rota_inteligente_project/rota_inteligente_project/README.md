# Rota Inteligente: Otimização de Entregas com Algoritmos de IA

**Resumo:** Projeto completo para a disciplina *Artificial Intelligence Fundamentals* — solução para a empresa fictícia **Sabor Express**. Implementa geração de mapa (grafo urbano), algoritmos de busca (A*, BFS), clustering (K-Means), heurística de roteamento e visualizações. Repositório pronto para ser enviado ao GitHub (contém código, dados, imagens e instruções).

## Estrutura do repositório
```
/src                # código-fonte (scripts Python)
/data               # datasets gerados (CSV)
/outputs            # imagens e gráficos gerados automaticamente
README.md
requirements.txt
run_all.sh          # script para reproduzir todo o processo localmente
pitch_script.txt    # roteiro do vídeo pitch (até 4 minutos)
```

## Objetivos
- Gerar um mapa simplificado da área de entrega como um grafo;
- Agrupar pedidos próximos usando K-Means;
- Calcular rotas eficientes entre múltiplos pontos usando A* e heurística de vizinho mais próximo por cluster;
- Produzir visualizações que comprovem ganhos de eficiência;
- Documentar decisões, limitações e sugestões de melhoria.

## Como executar (passo a passo)
1. Clone o repositório: `git clone <repo-url>`
2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate    # windows
```
3. Instale dependências:
```bash
pip install -r requirements.txt
```
4. Execute tudo (gera dados + imagens): 
```bash
bash run_all.sh
```
Os outputs (imagens, CSVs) ficarão em `/outputs`.

## Parte Teórica (README resumido)
- **Descrição do problema:** Otimizar rotas de entregadores para reduzir tempo e custo, considerando o mapa como grafo com pesos tempo/distância.
- **Abordagem adotada:** 
  - Geração de mapa planar (grid com pequenas variações de peso) usando `networkx`.
  - Clustering dos pontos de entrega com `KMeans` para agrupar entregas próximas e limitar rota por entregador.
  - Cálculo de rotas: A* para caminhos entre pares de nós no grafo; para sequência de entregas por cluster usei heurística nearest-neighbor (NN) aplicada aos nós do cluster, resolvendo o subtour com A* para cada trecho.
  - Métricas: distância total percorrida, número médio de nós visitados, tempo estimado (simulado a partir de pesos).

## Algoritmos usados
- **A\***: encontra menor caminho entre dois nós em grafos ponderados; utiliza heurística Euclidiana no grid.
- **BFS/DFS**: incluídos como utilitários (comparação básica em grafos não ponderados se necessário).
- **K-Means**: agrupa entregas em K clusters. `K` pode ser escolhido automaticamente com o método do cotovelo (script inclui opção automática).

## Diagrama do grafo
O diagrama do grafo é gerado automaticamente pelo script `src/01_generate_map_and_data.py` e salvo em `/outputs/graph_map.png`.

## Análise de resultados e limitações
(Resumo)
- Em cenários testados, agrupar entregas por K-Means reduz distância total quando comparado ao roteamento ingênuo sem agrupamento.
- Limitações: modelo simplificado do tráfego (pesos fixos), não considera janelas de tempo, capacidade por entregador, nem tráfego em tempo real. Para produção: integrar dados de tráfego, usar VRP (Vehicle Routing Problem) com MILP/OR-Tools, considerar aprendizado por reforço para roteamento dinâmico.

---
Para mais detalhes técnicos veja os scripts em `/src` e o `pitch_script.txt` para gravar seu vídeo.

