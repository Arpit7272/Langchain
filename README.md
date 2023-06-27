OBJECTIVE:

This utitity is for extending the use of OPENAI LLM to work on local database and also to extend search with external data like Google API.


INSTRUCTIONS TO RUN:

1. Install venv for python  --> my_env is virtual environment name
  python3 -m venv my_env

2. Activate virtual environment
  source my_env/bin/activate

3. Download the python packages
  pip install -r requirement.txt or
  pip3 install -r requirement.txt
--> If any package is missing use:
  pip install <package_name> or
  pip3 install <package-name>

4. Rename demo_config.py file with config.py and update the keys


FILES AND THEIR RESPONSE:

1. Langchain/pdf_from_directory.py:
--> This will read files one by one from Langchain/fileloader
--> Execute this with command below
  python Langchain/pdf_from_directory.py
--> Output: 
  FILE LOADED:  Rezmovits_Practical Psychopharm-Volume 1_Natural Meds_02.18.2022 (.75).pdf
  Type your question. Type 'exit' to stop.Type 'skip' to next document.  

--> skip will load the next document in folder and exit will exit the code
