from ai_api_wrapper import backend_google as googleai
from ai_api_wrapper import backend_openai as openaiai
from ai_api_wrapper import backend_anthropic as anthropicai

import pandas as pd
import os
import requests
import json
from dotenv import load_dotenv
import time 

# Load environment variables from .env file (optional but recommended)
load_dotenv()

def classify_comments(corpus_file, n_of_comments=150):    
    # Load CSV file with the corpus. The corpus is in the "Description" column.
    df = pd.read_csv(corpus_file) 
    if "Description" not in df.columns:
        raise ValueError("CSV file must contain 'Description' column.")
    
    output = {}
    
    topics = [
        "Responsabilidade da Braskem",
        "Crime ambiental",
        "Omissão dos órgãos públicos",
        "Disputa política",
        "Impacto na população",
        "Acordo da Braskem",
        "Relatório da CPI",
        "Mina 18",
        "Colpaso Mina",
        "Afundamento do solo",
        "Reparação das vítimas",
        "Corrupção",
        "Justiça e indenização",
        "Petrobras Odebrecht",
        "Estado Omisso",
        "Lira e Calheiros",
        "Falta de credibilidade da CPI",
        "Exploração gananciosa"
    ]
  
    count = 0
    for comment in df["Description"].dropna().astype(str).tolist():
        print(f"{comment}")              
        
        prompt = f"""
        Você é um especialista em análise de discurso e redes sociais.
        Os dados que você trabalha são comentários de redes sociais sobre a CPI da Braskem no Senado.

        Sua tarefa é atribuir, no mínimo, um e, no máximo, três tópicos ao comentário em <comentario>. 
        Utilize apenas os tópicos da lista de tópicos em <topicos>.

        Retorne apenas o(s) tópico(s) atribuídos no seguinte formato JSON:
        {{
            "Topics": ["tópico 1", "tópico 2", "tópico 3"]
        }}

        Não acrescentar nada à sua resposta, apenas o conteúdo do JSON.
        
        <comentario>{comment}</comentario> 
        <topicos>{topics}</topicos>
        """
        
        googleai_model = 'gemini-2.0-flash'
        comment_topics_raw = googleai.get_completion(prompt, googleai_model, display_config=False)
        
        # Remove any ```json or ``` markers from the response
        comment_topics_raw = comment_topics_raw.replace('```json', '').replace('```', '').strip()
        
        try:
            comment_topics = json.loads(comment_topics_raw)["Topics"]
            output[comment] = comment_topics
        except (json.JSONDecodeError, KeyError):
            output[comment] = "Erro ao classificar o comentário"
            
        # print(output)
        count += 1
        if count >= n_of_comments:
            break
    
    output_file_name = corpus_file.replace(".csv", f"_comment_topics_{googleai_model.replace('.', '_')}.json")
    with open(output_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)
    print(f"JSON file written to: {output_file_name}")
    
    # Store the output as an Excel file
    output_excel_name = corpus_file.replace(".csv", f"_comment_topics_{googleai_model.replace('.', '_')}.xlsx")
    df_output = pd.DataFrame([(k, ', '.join(v)) for k, v in output.items()], columns=['Comment', 'Topics'])
    df_output.to_excel(output_excel_name, index=False)
    print(f"Excel file written to: {output_excel_name}")

def topic_modeling(corpus_file):
    
    # Load CSV file with the corpus. The corpus is in the "Description" column.
    df = pd.read_csv(corpus_file) 
    if "Description" not in df.columns: 
        raise ValueError("CSV file must contain 'Description' column.")
    # Combine the "Description" texts into a single string, separated by newlines.
    corpus = "\nINICIO_DE_COMENTARIO: ".join(df["Description"].dropna().astype(str).tolist())  
    # print(f"Corpus is: {corpus}")
    
    prompt = f"""
            Você é um especialista em análise de discurso e redes sociais.
            O corpus são comentário de redes sociais sobre a CPI da Braskem no Senado brasileiro. 
            O corpus está em <corpus> onde cada cometário começa em INICIO_DE_COMENTARIO.

            Sua tarefa é fazer a modelagem de tópicos e retorne os tópicos que mais se destacam.
            Utilize uma abordagem indutiva (leitura exploratória para identificar os tópicos principais).
            Os tópicos devem ser concisos (no máximo 3 palavras).
            Seja criterioso na escolha dos tópicos, pois eles devem refletir com precisão
            os argumentos e temas presentes no corpus.   
            Retorne apenas a lista dos tópicos como uma lista de string em Python.

            <corpus>{corpus}</corpus>
        """    
    
    # print(f"Prompt is:\n{prompt}")    
    # Salva o prompt em arquivo 
    prompt_file_name = corpus_file.replace(".csv", "_prompt.txt")
    with open(prompt_file_name, "w") as f:
        f.write(prompt)

    # Número aproximado de tokens do prompt
    token_count = int( len(prompt) / 4 ) 
    print(f"Number of tokens: {token_count}" + "\n")

    # WARNING: Might take a while between model calls due to Gemini timeouts, eg, 5 RPM (requests per minute)
    googleai_models = ['gemini-1.5-pro-002', 'gemini-2.0-pro-exp-02-05', 'gemini-2.0-flash', 'gemini-2.0-flash-thinking-exp-01-21']
    for googleai_model in googleai_models:
        print(f"Before calling Gemini API, model is: {googleai_model}")
        # Topic Modeling with Google Gemini
        topics = googleai.get_completion(prompt, googleai_model, display_config=False)
        # print(f"\nTopic list is:\n{topics}")
        # Save topics to a text file
        topics_file_name = corpus_file.replace(".csv", f"_topics_{googleai_model.replace('.', '_')}.txt")
        with open(topics_file_name, "w") as f:
            f.write(topics)

    # # Topic Modeling with OpenAI o3
    # openaiai_model = "o3-mini" 
    # topics = openaiai.get_completion(prompt, openaiai_model, display_config=False)
    # # Save topics to a text file
    # topics_file_name = corpus_file.replace(".csv", "_topics_o3_mini.txt")
    # with open(topics_file_name, "w") as f:
    #     f.write(topics)    

    # # Topic Modeling with Anthropic Claude
    # anthropicai_model = "claude-3-7-sonnet-20250219"
    # topics = anthropicai.get_completion(prompt, model=anthropicai_model, display_config=False)
    #  # Save topics to a text file
    # topics_file_name = corpus_file.replace(".csv", "_topics_clause_3_7_sonnet.txt")
    # with open(topics_file_name, "w") as f:
    #     f.write(topics)
    
    
    return topics
        
        
def main():
    dataset = "./dataset/braskem_dataset_IG.csv"
    # topic_modeling(dataset)
    classify_comments(dataset)
    return None

if __name__ == "__main__":
    main()

