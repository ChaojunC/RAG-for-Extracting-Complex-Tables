# RAG for Extracting Complex Tables

### Objective
Create a Python pipeline that demonstrates document processing capabilities, focusing on ingesting PDF documents containing tables and integrating them with a Large Language Model (LLM) for query-based information retrieval.

### RAG Pipeline

#### 1. Document Processing
- **PDF Document Ingestion**: Implement the ingestion of PDF documents, with a special focus on extracting tables.
- **Table Parsing**: Use the LLM to parse tables within the documents and extract structured data.
- **Superscript Relations**: Relate superscripts in table columns to their references.

**File**: `llm_parse_complex_table.py`  
**Description**: Parses complex tables within PDF documents.

**Output**: 
The first image is the input table while the second image is the llm output for parsing complex table. Note that this llm approach is a significant improvement compare to traditional methods:

Complex table:
<figure>
  <img src="./image/table_ori.png" alt="A description of the image" style="width:65%">
</figure>

Extracting complext table using llm
<figure>
  <img src="./image/llm_table.png" alt="A description of the image" style="width:75%">
</figure>

**File**: `llm_parse_pdf.py`  
**Description**: Extracting information from tables in pdf ("./document/Type_II_table.pdf") for generating knowledge graph.

<figure>
  <img src="./image/llm_kg_table.png" alt="A description of the image" style="width:35%">
</figure>

#### 2. LLM Inference
- **User Prompt Handling**: handle user prompts.
- **RAG Model Integration**: Integrate with a Retrieval-Augmented Generation (RAG) model to generate responses based on user queries.
- **Information Retrieval**: Retrieve relevant information from the ingested documents to include in the responses.

**File**: `llm_multi_doc.py`  
**Description**: Conducts real-time Q&A across multiple documents using RAG and LLM. Can be used to extract information and identify connections between different documents. It can also serves as a tool for onboarding to swiftly familiarize new employees with the company or for quick internal search of comapny documents.

**Output Example**: 
Conduct real-time Q&A across multiple documents using RAG and LLM
<figure>
  <img src="./image/llm_q&a.png" alt="A description of the image" style="width:70%">
</figure>

#### 3. Knowledge Graph Generation
- **Knowledge Graph**: Generate a knowledge graph from the retrieved document evidence.

**File**: `llm_main.py`  
**Description**: Contains the entire process and generates the json file for Knowledge Graph visualization at the end.

**Output Example**: 
json file for knowledge graph visualization
<figure>
  <img src="./image/llm_kg.png" alt="A description of the image" style="width:35%">
</figure>

### Usage
1. **Knowledge Graph json file Generation**:
    - Run `llm_main.py` to parse tables from the PDF documents and generate knowledge graph.
      
    ```bash
    python llm_main.py
    ```
2. **LLM Inference**:
    - Run `llm_multi_doc.py` to perform real-time Q&A and retrieve information.
      
    ```bash
    python llm_multi_doc.py
    ```
3. **Knowledge Graph Visualization**:
    - Run the following command to visualize the generated knowledge graph inside folder kg-demo.
      
    ```bash
    npm start
    ```

### Generated Knowledge Graph
[knowledge graph visualization](./image/knowledge_graph.pdf)

### Appendix
The previous method proves inadequate for handling complex tables. I have also explored GitHub repositories such as nlmatics/nlm-ingestor, nlmatics/llmsherpa, and Joshua-Yu/graph-rag for PDF parsing and table extraction, as recommended. Currently, llm_parse_table.py, demonstrates the best performance when it comes to handling complex table.

Complext table
<figure>
  <img src="./image/table_ori2.png" alt="A description of the image" style="width:50%">
</figure>

Extracting complex table using previous method
<figure>
  <img src="./image/extract_table.png" alt="A description of the image" style="width:50%">
</figure>
