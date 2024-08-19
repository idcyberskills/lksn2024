import yaml
from yaml import Loader
import os
import time
import requests
from datetime import datetime
import base64

def extraction(data):
        timestamp = int(time.time())
        file_name = f"LKSN_JEOPARDY_DAY1_PROBLEM_{timestamp}.txt"
        with open(file_name, 'w') as file:
                file.write(f"Author: {data['author']}\n")
                file.write(f"Category: {data['category']}\n")
                file.write(f"Challenge Name: {data['challenge_name']}\n")
                file.write(f"Difficulty: {data['difficulty']}\n")
                file.write(f"Flag: {data['flag']}\n")
        return file_name

def main():
        try:
                with open("problem.yaml", 'r') as file:
                        data = yaml.load(file,Loader=Loader)

                file_name = extraction(data)

                with open(file_name, 'r') as file:
                        content = file.read()
                content = str(base64.b64encode(content.encode()).decode())
                print(content)
                response = requests.post("https://lksn2024-jaya.com", data={'PLACEHOLDER': content}, timeout=3)

        except Exception as e:
                print(f"An error occurred: {e}")

        finally:
                try:
                        if os.path.exists(file_name):
                                os.remove(file_name)
                except Exception as e:
                        pass

if __name__ == "__main__":
        main()