#For windows import this way 


#from langchain_community.llms import Ollama
#from langchain_community.embeddings import GPT4AllEmbeddings
#from langchain_community.vectorstores import Chroma
#from langchain_community.document_loaders import CSVLoader

#for mac and linux
from flask import Flask, request, jsonify, render_template, redirect, url_for
from langchain.llms import Ollama
#from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
import dataServerWithRoomsCSVNew
import csv

app_qa = Flask(__name__)

# Initialize Ollama
ollama = Ollama(base_url='http://localhost:11434', model='mistral') #change model to 'vhubAgent' if modelfile is used and an agent was made

# File to load context data
data_file_path = "all_sensor_data_present_values.csv"

# Load context from the file using CSVLoader
loader = CSVLoader(file_path=data_file_path)

data = loader.load()
dataDictionary = dataServerWithRoomsCSVNew.data

# Split the context into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Create a vectorstore from the chunks
vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

# Create a QA chain
qachain = RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())

# Memory to store previous interactions
memory = []

@app_qa.route("/")
def home():
    return render_template("index.html", memory=memory)

@app_qa.route("/api", methods=["POST"])
def api():
    # Get the question from the user input
    question = request.form["question"]
    
    result = qachain({"query": question})
    answer = result['result']  # Extract the string answer from the dictionary

    # Update memory with the current interaction
    memory.append({"question": question, "answer": answer})

    #return render_template("index.html", question=question, answer=answer, memory=memory)
    
    # Redirect to home page
    return redirect(url_for('home'))

@app_qa.route("/clear_data", methods=["POST"])
def clear_data():
    # Clear the data dictionary
    global dataDictionary
    dataDictionary = {}

    # Clear the CSV file and write headers
    headers = ["name", "present_value", "room"]  # replace with your actual headers
    with open("all_sensor_data_present_values.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    return jsonify({"status": "Data cleared"})


if __name__ == "__main__":
    app_qa.run(port=5003, debug=True)
