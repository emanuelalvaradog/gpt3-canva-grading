import os
import re
import openai
import codecs
import json

# Write the evaluation requirements
requirements = """Actividad: Básica
Crear un programa que me permita saber cuál es el competidor más veterano que ha recibido medalla (oro, plata o bronce)
Crear un programa que me permita saber cuál es el competidor más joven que ha recibido medalla de oro
Encuentra al competidor más ganador de la historia y crea un csv con toda su información.

Actividad: Avanzada
Crear un programa que me permita saber cuál es el competidor más veterano que ha recibido medalla para los NOC´s MEX, COL y ARG (oro, plata o bronce) 
Crear un programa que me permita saber cuál es el competidor más joven que ha recibido medalla de oro para los NOC´s USA y CAN
Encuentra al competidor más ganador de la historia en medallas totales, medallas de oro, medallas de plata y medallas de broce para los NOC´s USA, CHN y RUS. Crea un csv con toda su información.
"""

# Paste your OPENAI's API key
OPEN_AI_API_KEY = "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"

# Set the route where the ipynb files will be located
# default: ./submissions
FILES_PATH = "./submissions"


def retrieve_code_from_file(filename):
    try:
        f = codecs.open(filename, "r")
        json_file = json.loads(f.read())
        output_code = ""

        for x in json_file["cells"]:
            for x2 in x["source"]:
                output_code += x2
                if x2[-1] != "\n":
                    output_code += "\n"

        output_code = re.sub(r"#.*", "", output_code).strip()
    except:
        print("Error retrieve_code_from_file")
        return {"name": filename, "error": "Error retrieving code from file"}
    else:
        return output_code


def grade_code_with_gpt(code, filename):
    openai.api_key = OPEN_AI_API_KEY
    dict_res = {
        "name": filename,
    }
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Basado en los siguientes requerimientos: {requirements} califica el siguiente código en una escala de 0 a 10 y da feedback usando el siguiente formato \n Calificacion: \n Feedback: \n {code}",
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    except:
        print("Error grade_code_with_gpt")
        dict_res["error"] = "Error evaluating code with gpt"
        return dict_res
    else:
        try:
            json_response = json.loads(str(response))
            text_output = json_response["choices"][0]["text"].split("\n")
            text_output = [res for res in text_output if res]
            evaluation = dict(
                zip(
                    [res.split(": ")[0] for res in text_output],
                    [res.split(": ")[1] for res in text_output],
                )
            )

            dict_res = {**dict_res, **evaluation}
            return dict_res
        except:
            print("Error formating grade_code_with_gpt")
            dict_res["error"] = "Error formating evaluation response"
            return dict_res


def main():
    output_file = open("grade_results.json", "w")
    grades = []

    for filename in os.listdir(FILES_PATH):
        if filename.endswith(".ipynb"):
            print("---")
            file_path = os.path.abspath(os.path.join(FILES_PATH, filename))
            code = retrieve_code_from_file(file_path)
            if type(code) is dict:
                continue
            code += "\n"
            print(file_path)
            grade_res = grade_code_with_gpt(code, filename)
            if "error" in grade_res:
                pass
            grades.append(grade_res)

    json.dump(grades, output_file)


if __name__ == "__main__":
    main()
