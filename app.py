import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.llms.cohere import Cohere
from langchain.chains.question_answering import load_qa_chain

load_dotenv()

st.set_page_config(page_title="Ask your pdf")

st.title("Ask your :red[PDF]")

#upload file
pdf=st.file_uploader("Upload your pdf", type='pdf')


#extract the text
if pdf is not None:
    pdf_reader=PdfReader(pdf)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()

    #split into chunks
    text_splitter=CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks=text_splitter.split_text(text)
    
    #create embeddings
    embeddings=CohereEmbeddings(cohere_api_key=os.getenv("COHERE_API_KEY"))
    knowledge_base=FAISS.from_texts(chunks, embeddings)

    user_question=st.text_input("Ask a question about your PDF")
   

    if user_question:
       


        llm=Cohere()
        docs=knowledge_base.similarity_search(user_question)
        chain=load_qa_chain(llm, chain_type="stuff")
        response=chain.run(input_documents=docs, question=user_question)
        st.write(response)
        




