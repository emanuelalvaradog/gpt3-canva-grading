# **GPT3 Canva Grading**

### This tool simplifies grading canva assignments involving .ipynb

## **How to use?**

1. ### Make sure you have python installed in your computer
   (Depending on your OS you might want to try: py or python instead of python3)

```bash
python3 --version
"Python 3.X.X"
```

2. ### Install the required dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

3. ### Download all the submissions from canva using the "download submissions" button in every assignment. It should download a .zip file which has to be decompressed into a directory (default: submissions).

4. ### Run the python script and output the results. Output file is a .json file including name, grade and feedback. In case something went wrong grade and feedback will be ignored and a new value "error" will be returned

```bash
python3 script.py
```
