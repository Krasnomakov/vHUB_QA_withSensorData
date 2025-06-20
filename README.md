# WPVH AI Chat Solution 🤖

A retrieval QA solution for the WPVH Eindhoven AI chat, using real-time sensor data. This application is powered by the Mistral LLM model served via Ollama.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/LangChain-4A90E2?style=for-the-badge" alt="LangChain" />
  <img src="https://img.shields.io/badge/Ollama-lightgrey?style=for-the-badge" alt="Ollama" />
</p>

## 🎥 Demo

Check out the video demo: **[Watch Here](https://vimeo.com/907558591/310a7a27d4)**

## ✨ Features

- **Real-time Data QA**: Chat with an AI that has access to the latest sensor data.
- **Local LLM**: Uses a locally hosted Mistral model with Ollama for privacy and control.
- **Extensible**: Built with modular components using Flask and LangChain.
- **Vector Storage**: Utilizes ChromaDB for efficient similarity searches on sensor data.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **LLM & Tooling**: Ollama, LangChain, Mistral
- **Database**: ChromaDB (for vector storage)
- **Deployment**: Docker

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- **Python 3.x**
- **Ollama**: Install from [Ollama.ai](https://ollama.ai/).
  - **For Windows users**: Use the [Docker version of Ollama](https://hub.docker.com/r/ollama/ollama). Tutorial [here](https://youtu.be/y13OTgiZXdg?si=sC0X0Lh-OOY1ggHg).

### ⚙️ Installation & Running

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd vHUB_QA_withSensorData
    ```
    *Replace `<repository-url>` with the actual URL of this repository.*

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Ollama Model** (Skip for Windows)
    Create a system prompt for the LLM model:
    ```bash
    ollama create vhubAgent -f ./modelfile
    ```

4.  **Run Ollama**
    - **For Docker**: `docker exec -it ollama ollama run vhubAgent`
    - **For Windows (with Docker)**: `docker exec -it ollama ollama run mistral`

5.  **Enter Credentials**
    Open `keys.py` and enter your username and password for the vhub delta API.

6.  **Start the Servers**
    - **Data Server**: Open a terminal and run:
      ```bash
      python dataServerWithRoomsCSVNew.py
      ```
    - **Retrieval QA Server**: Open a *new* terminal and run:
      ```bash
      python ollamaWithDataCSV.py
      ```

🎉 Your chat application is now live at `http://localhost:5003`.

## ⚠️ Important Notes

- **Clear Data**: Use the `clear data` button in the UI to prevent overwhelming the data server. The dataframe will need some time to repopulate with new values.
- **Threading**: The application uses a semaphore to limit concurrent threads to 100 for fetching sensor data. This can be adjusted in `dataServerWithRoomsCSVNew.py`.
- **Sensor Limit**: There are 191 sensors in `sensors_list.txt`. Increasing the thread limit in `threading.Semaphore(100)` to `191` to fetch all data concurrently may lead to instability, such as saving incorrect values or injecting empty data.

## ☁️ Deployment

For deployment options and requirements, refer to the [Google Document](https://docs.google.com/document/d/1LrkOkPiyaTB3qdNpzFsY5K6ZIQ1q8DNc73nApcfB6zU/edit?usp=sharing).
