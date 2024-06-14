import PyPDF2
import openai
import os

# Replace with your OpenAI API key and model
openai.api_key = "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"
my_ai_model = "gpt-4o"

pdf_file = "/content/Complex_table_variant_3_rotated.pdf"

def aiprocessor(page_no, text):
    print(f"\n\n..AI processing page {page_no}")
    messages = [
        {
            "role": "system",
            "content": """You are a PDF table extractor, a backend processor.
- The goal is to identify tabular data, and reproduce it cleanly as table.
- Some column titles have subtitles. Treat subtitles as different columns Do not merge any columns
- Preface each output table with a line giving title and 10 word summary.
- Reproduce each separate table found in page."""
        },
        {
            "role": "user",
            "content": "raw pdf text; extract and format tables:" + text
        }
    ]

    client = openai.OpenAI(
        api_key=openai.api_key
    )

    api_params = {"model": my_ai_model, "messages": messages}
    try:
        api_response = client.chat.completions.create(**api_params)
        
        reply = ""
        print(api_response.choices[0].message.content)
        
        return api_response.choices[0].message.content
    except Exception as err:
        error_message = f"API Error page {page_no}: {str(err)}"
        print(error_message)

# Create a list to store AI-processed text
ai_processed_text_list = []

# Open the PDF file in binary mode
with open(pdf_file, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    print(len(pdf_reader.pages))

    # Iterate through each page and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()

        if len(page_text)>20:
            # Dump unprocessed pages if desired
            page_text_file = pdf_file.name + "-extractedpage" + str(page_num) + ".txt"
            with open(page_text_file, 'w', encoding='utf-8') as output_file:
                output_file.write(page_text)

            # Process with AI
            ai_processed_text = aiprocessor(page_num, page_text)

            # Dump AI pages if desired
            page_text_file = pdf_file.name + "-AIpage" + str(page_num) + ".txt"
            with open(page_text_file, 'w', encoding='utf-8') as output_file:
                output_file.write(page_text)

            # Append the AI-processed text to the list
            ai_processed_text_list.append(ai_processed_text)

# Combine all AI-processed text into a single string
combined_text = "\n".join(ai_processed_text_list)

# Define the output text file name (same root name as the PDF)
output_text_file = pdf_file.name + "-AI-all.txt"

# Save the combined text into a .txt file
with open(output_text_file, 'w', encoding='utf-8') as output_file:
    output_file.write(combined_text)

print(f"AI-processed text saved to {output_text_file}")