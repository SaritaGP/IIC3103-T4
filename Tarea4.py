import requests
import gspread
import xml.etree.ElementTree as ET
import pandas as pd
from gspread_dataframe import set_with_dataframe


codigos_paises = ['FRA', 'CHL', 'GRC', 'USA', 'DEU', 'RUS']

gc = gspread.service_account(filename='credenciales.json')
sh = gc.open_by_key('1LPIT9Iu9Rgo-sNPQlOwbgpX05zEMibgRxP5_yTZ39j4')
worksheet = sh.sheet1

nodos = ['GHO', 'COUNTRY', 'SEX', 'YEAR', 'GHECAUSES',
         'AGEGROUP', 'Display', 'Numeric', 'Low', 'High']
indicadores = ['Number of deaths',
               'Number of infant deaths', 'Number of under-five deaths', 'Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)', 'Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)', 'Estimates of number of homicides', 'Crude suicide rates (per 100 000 population)', 'Mortality rate attributed to unintentional poisoning (per 100 000 population)', 'Number of deaths attributed to non-communicable diseases, by type of disease and sex', 'Estimated road traffic death rate (per 100 000 population)', 'Estimated number of road traffic deaths', 'Mean BMI (kg/m&#xb2;) (crude estimate)', 'Mean BMI (kg/m&#xb2;) (age-standardized estimate)', 'Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)', 'Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)', 'Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)', 'Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)', 'Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)', 'Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)', 'Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)', 'Estimate of daily cigarette smoking prevalence (%)', 'Estimate of daily tobacco smoking prevalence (%)', 'Estimate of current cigarette smoking prevalence (%)', 'Estimate of current tobacco smoking prevalence (%)', 'Mean systolic blood pressure (crude estimate)', 'Mean fasting blood glucose (mmol/l) (crude estimate)', 'Mean Total Cholesterol (crude estimate)']

filas = []


dic = {'GHO': [], 'COUNTRY': [], 'SEX': [], 'YEAR': [], 'GHECAUSES': [],
       'AGEGROUP': [], 'Display': [], 'Numeric': [], 'Low': [], 'High': []}

sh.values_clear("A1:J30000")

for pais in codigos_paises:
    xml_orginal = requests.get(
        'http://tarea-4.2021-1.tallerdeintegracion.cl/gho_'+pais+'.xml')
    xml_escrito = open('reporte.xml', 'wb')
    xml_escrito.write(xml_orginal.content)
    xml_escrito.close()
    tree = ET.parse('reporte.xml')
    root = tree.getroot()
    for facts in root:
        if facts.find('GHO').text in indicadores:
            fila = []
            for nodo in nodos:
                try:
                    if type(facts.find(nodo).text) != 'NoneType':
                        if nodo == 'Numeric' or nodo == 'Low' or nodo == 'High':
                            dic[nodo].append(float(facts.find(nodo).text))
                        else:
                            dic[nodo].append(facts.find(nodo).text)
                    else:
                        dic[nodo].append(' ')
                except:
                    dic[nodo].append(' ')

df = pd.DataFrame(dic)
print('procesamiento de datos listo')

set_with_dataframe(worksheet, df)
print('sheet escrita')
