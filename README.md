# ToniGPT
Hiermit lassen sich Audiogeschichten für Kinder erstellen. 
Die Kinder können sich aus vorgegeben Keywörtern ihre Geschichten in verschiedenen Genre erstellen lassen. 

Letzendlich wird ein Prompt zusammengesetzt, der über die OpenAI API an ChatGPT gesendet wird. Dort wird die Geschichte
erzeugt und mit dieser wird via TTS (aktuell OpenAI TTS) ein mp3 File erzeugt. 

Das ganze ist als Flask-APP aufgesetzt und kann auch in einem Dockercontainer laufen. 

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You need to have an OpenAI API Key

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://openai.com](https://openai.com)
2. Clone the repo
   ```js
   git clone https://github.com/flomet/ToniGPT.git
   ```
3. Create an empty `.env` file and enter your OpenAI API Key
   ```js
   OPENAI_API_KEY=your_key
   ```
4. For a local test also enter the path where the stories should be stored in the `.env` (this should not be done for a Docker deploy)
   ```js
   STORIES_DIR=./stories
   ```   
5. Install the dependencies from the requirements.txt
  ```js
   pip install requirements.txt
   ```  
6. Run the app
  ```js
   python tonigpt_app.py
   ``` or 
  ```js
   flask --app my_flask_app run --debug
   ``` 
 
   

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>







