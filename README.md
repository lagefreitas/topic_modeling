# Modelagem de Tópicos em Redes Sociais com IA Generativa

Este repositório contém o código e material reproduzível da pesquisa sobre **Análise de Conteúdo de Redes Sociais Durante a CPI da Braskem** usando técnicas de Inteligência Artificial Generativa.


Projeto em colaboração entre o [Labinove - Laboratório de Pesquisa Aplicada e Inovação Tecnológica](dgp.cnpq.br/dgp/espelhogrupo/2916559158183746) e o [Grupo de Pesquisa Baleia](http://instagram.com/baleiaufal). Em caso de dúvidas, entrar em contato com o Prof. André Lage ([Instagram](https://www.instagram.com/prof.lage), [Linkedin](http://linkedin.com/in/lage), [E-mail](mailto:andre.lage@ichca.ufal.br)).


## Funcionalidades

- **Modelagem de Tópicos**: Análise exploratória de tópicos em comentários de redes sociais usando diferentes modelos de IA do Google Gemini:

```
'gemini-1.5-pro-002', 'gemini-2.0-pro-exp-02-05', 'gemini-2.0-flash', 'gemini-2.0-flash-thinking-exp-01-21'
```

- **Classificação de Comentários**: Categorização automatizada de comentários em tópicos pré-definidos utilizando o modelo `gemini-2.0-flash`.

## Requisitos

- Python 3.x
- Bibliotecas: pandas, requests, python-dotenv
- APIs: Google AI, OpenAI, Anthropic

## Configuração

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o arquivo `.env` com suas chaves de API

## Uso

```python
from ai_api_wrapper import backend_google as googleai

# Modelagem de tópicos
topic_modeling("seu_arquivo.csv")

# Classificação de comentários
classify_comments("seu_arquivo.csv", n_of_comments=150)
```

## Estrutura dos Dados

O arquivo CSV de entrada deve conter uma coluna "Description" com os comentários a serem analisados.
