# WPVH AI Chat Solution

This repository hosts a retrieval QA solution for WPVH Eindhoven AI chat, developed using the Mistral LLM model via the Ollama application.

**Demo:** https://vimeo.com/907558591/310a7a27d4

## Getting Started

1. **Install Ollama**: Visit [Ollama.ai](https://ollama.ai/) to install Ollama. For Windows, use the Docker version. You can find a tutorial [here](https://youtu.be/y13OTgiZXdg?si=sC0X0Lh-OOY1ggHg) and the Docker image [here](https://hub.docker.com/r/ollama/ollama).

2. **Clone this Repository**: Use `git clone` to download this repository.

3. **Navigate to the Directory**: Use `cd vhubRetrievalQA` to navigate to the relevant directory.

4. **Create a System Prompt for the LLM Model**: Run `ollama create vhubAgent -f ./Modelfile` inside the directory. Skip this step for Windows.

5. **Run Ollama**: Use `docker exec -it ollama ollama run vhubAgent` for Docker or `docker exec -it ollama ollama run mistral` for Windows.

6. **Open a New Terminal Window**: Navigate to the same directory using `cd vhubretrievalqa`.

7. **Enter Your Credentials**: Open `keys.py` and enter your username and password for the vhub delta API.

8. **Run the Data Server**: Execute `python dataServerWithRoomsCSVNew.py`.

9. **Run the Retrieval QA Server**: Open a new terminal window and run `python ollamaWithDataCSV.py`.

The above steps will launch a chat accessible at `localhost:5003`. Use the app to chat about data from WPVH sensors. The chat history is displayed, but the model is not aware of it.

## Important Notes

- Use the `clear data` button to prevent overwhelming the data server. After clearing, some time will be needed to fill the dataframe with new values.
- The code uses threads, limited to 100, keeping the number of actively updating sensors around 100. If you increase this number in `dataServerWithRoomsCSVNew` by changing `semaphore = threading.Semaphore(100)`, it will become more demanding. There are 191 sensors in the `sensor_list.txt` file. To get all of them concurrently updating, the Semaphore Object must also reach 191. However, this number creates too many concurrent threads and causes bugs in the program, such as saving wrong values and injecting empty values into the dataframe.

## Deployment Options and Requirements

For deployment options and requirements, refer to this [Google Document](https://docs.google.com/document/d/1LrkOkPiyaTB3qdNpzFsY5K6ZIQ1q8DNc73nApcfB6zU/edit?usp=sharing).
