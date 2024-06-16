from langchain.docstore.document import Document
import openai
import json
import os
from llm_parse_pdf import llm_parse_table
from dotenv import load_dotenv
from pathlib import Path


# Get the OpenAI API key from environment variables
load_dotenv('.env.example')
openai.api_key = os.getenv('OPENAI_API_KEY')


def load_docs_from_jsonl(file_path):
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array


def find_relation_for_subtype(subtype, text, model):
    messages = [
        {
            "role": "system",
            "content": """You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible
    using the context text provided. Your answers should only answer the question once and not have any text after
    the answer is done."""
        },
        {
            "role": "user",
            "content": f"""Find all relations to the logical record type {subtype}.

            only list the relationship if there is a value such as "2.005 RET is 1". If the relationship is "2.003 FFN is" Don't include the 
            subfield in the relationship.

            Must list relationships in the format: [ENTITY 1, ENTITY TYPE, RELATION, ENTITY 2, ENTITY 2 TYPE].
              - Do not number the results in the list.
              - ENTITY TYPES are: "subtype" and "subfield".
              - RELATIONSHIPS are defined as "has subfield" (linking a subfield to its subtype).
            For example:

            ["AMN", "subtype", "has subfield", "2.001 LEN", "subfield"]
            ["AMN", "subtype", "has subfield", "2.002 IDC", "subfield"]

            Here are the given input text:
            """ + text
        }
    ]

    client = openai.OpenAI(
        api_key=openai.api_key
    )

    api_params = {"model": model, "messages": messages}

    api_response = client.chat.completions.create(**api_params)
    
    print(api_response.choices[0].message.content)
    
    return api_response.choices[0].message.content


if __name__ == "__main__":
    model = "gpt-4o"
    file = "./document/Type_II_table.pdf"

    #Parse table
    llm_parse_table(file, model)
    text = Path('processed_table.txt').read_text()

    subtype_dict = [item.strip().strip("\n") for item in open("subtypes_dict.txt", "r").readlines()]

    #Find connection
    relations = []
    for subtype in subtype_dict:
        raw_curr_relations = find_relation_for_subtype(subtype, text, model)
        cleaned_curr_relations = [item.strip().strip(",").strip("[").strip("]").split(",") for item in raw_curr_relations.split("\n")]
        print(cleaned_curr_relations)
        formatted_json_list_curr = [{
            "source": item[0],
            "sourcetype": item[1],
            "relation": item[2],
            "target": item[3],
            "targettype": item[4]
        } for item in cleaned_curr_relations]
        print(formatted_json_list_curr)
        relations.extend(formatted_json_list_curr)

    with open('./kg/kg-demo/src/kg_relations.json', 'w') as file:
        json.dump(relations, file, indent=4)
