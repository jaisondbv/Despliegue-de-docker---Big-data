import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px


def extraer_primeros_4_digitos(año):
  
    año_limpio = re.sub(r"[^\d]", "", año)
   
    return año_limpio[:4]


url = "https://es.wikipedia.org/wiki/Bal%C3%B3n_de_Oro"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


tables = soup.find_all("table", {"class": "wikitable"})
ballon_dor_data = []


for row in tables[0].find_all("tr")[1:]:
    cols = row.find_all("td")
    if len(cols) >= 2:
        year = cols[0].text.strip()
        player = cols[1].text.strip()
        ballon_dor_data.append([year, player])


df = pd.DataFrame(ballon_dor_data, columns=["Año", "Jugador"])


df["Año"] = df["Año"].apply(extraer_primeros_4_digitos)


df["Año"] = df["Año"].astype(int)


df["Jugador"] = df["Jugador"].str.title()


fig = px.scatter(df, x="Año", y=[1] * len(df), text="Jugador", title="Línea de Tiempo de los Ganadores del Balón de Oro")


fig.update_traces(marker=dict(size=12, color='red'), textposition='top center')


fig.update_layout(
    yaxis=dict(showticklabels=False),
    xaxis_title="Año",
    showlegend=False
)


fig.show()


# df.to_csv("C:/Users/204/Downloads/ganadores_balon_de_oro_hecho_por_jaison.csv", index=False, encoding='utf-8-sig')

df.to_csv("ganadores_balon_de_oro.csv", index=False, encoding='utf-8-sig')


