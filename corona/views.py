from django.shortcuts import render, get_object_or_404
from .models import contact, Blog
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objs as go

page = requests.get('https://www.worldometers.info/coronavirus/')
soup = BeautifulSoup(page.content, 'html.parser')

cdc = soup.find_all(class_='maincounter-number')

Tcase = cdc[0]
cases = Tcase.get_text()

Tdeath = cdc[1]
deaths = Tdeath.get_text()

Tcured = cdc[2]
cured = Tcured.get_text()

table = soup.find('table', id="main_table_countries_today")
headers = [heading.text.replace(",Other", "") for heading in table.find_all('th')]
table_rows = [row for row in table.find_all('tr')]

results = [{headers[index]: cell.text for index, cell in enumerate(row.find_all("td"))} for row in table_rows]

for i in results:
    if "Country" in i:
        if i["Country"] == "Saudi Arabia":
            Saudiall = i

for i in results:
    if "Country" in i:
        if i["Country"] == "USA":
             USAall = i

for i in results:
     if "Country" in i:
          if i["Country"] == "Italy":
             Italyall = i

for i in results:
     if "Country" in i:
           if i["Country"] == "France":
              Franceall = i

for i in results:
      if "Country" in i:
         if i["Country"] == "Spain":
            Spainall = i

Sacase, Sadeath, Sacure = Saudiall["TotalCases"].replace(',', ''), Saudiall["TotalDeaths"].replace(',', ''), \
                              Saudiall["TotalRecovered"].replace(',', '')

USAcase, USAcure = USAall["TotalCases"].replace(',', ''), USAall["TotalRecovered"].replace(',', '')
Italycase, Italycure = Italyall["TotalCases"].replace(',', ''), Italyall["TotalRecovered"].replace(',', '')
Francecase, Francecure = Franceall["TotalCases"].replace(',', ''), Franceall["TotalRecovered"].replace(',', '')
Spainacase, Spaincure = Spainall["TotalCases"].replace(',', ''), Spainall["TotalRecovered"].replace(',', '')

""" Below is the return so u can easily add it again 
"""




def about(request):
    return render(request, 'corona/about.html')


def about_covid(request):
    return render(request, 'corona/about_covid-19.html')


def blogs(request):
    var_1 = Blog.objects.all()
    return render(request, 'corona/blogs.html', {'var_1': var_1})


def detail(request, blog_id):
    detail_page = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'corona/detail.html', {'detail_blog': detail_page})


def Contact(request):
    if request.method == 'POST':
        Your_name = request.POST.get('name')
        Your_email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Your_Message = request.POST.get('messages')

        var_contact = contact(name=Your_name, email=Your_email, subject=Subject, messages=Your_Message)
        var_contact.save()
        return render(request, 'corona/thanks.html')
    else:
        return render(request, 'corona/contact.html')


def M_Home(request):
    return render(request, 'corona/index.html',
                  {'cases': cases, 'deaths': deaths, 'cured': cured, 'Sacase': Sacase, 'Sadeath': Sadeath,
                   'Sacure': Sacure, 'UScase': USAcase, 'UScure': USAcure, 'ITcase': Italycase, 'ITcure': Italycure,
                   'FRcase': Francecase, 'FRcure': Francecure, 'SPcase': Spainacase, 'SPcure': Spaincure})


def M_Cases(request):
    page = requests.get('https://www.worldometers.info/coronavirus/')

    soup = BeautifulSoup(page.content, 'html.parser')

    Location = []
    Cases = []
    df = pd.DataFrame(columns=["Location", "Cases"])

    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')
        Location.append(td[0].text)
        Cases.append(td[1].text)

    df = pd.DataFrame({'Location': Location, 'Cases': Cases})

    df.to_csv("Corona.csv", index=False)

    for k in range(len(Cases)):
        Cases[k] = Cases[k].translate({ord(','): None})

    Cases[7] = ''

    fig = go.Figure(data=go.Choropleth(
        locations=df['Location'],
        locationmode='country names',
        z=Cases,
        colorscale='Reds',
        marker_line_color='black',
        marker_line_width=0.5,
    ))
    fig.update_layout(
        title_text='Corona Virus (Total Cases)',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    data = fig.show()
    return render(request, 'corona/index.html',
                  {'cases': cases, 'deaths': deaths, 'cured': cured, 'Sacase': Sacase, 'Sadeath': Sadeath,
                   'Sacure': Sacure, 'UScase': USAcase, 'UScure': USAcure, 'ITcase': Italycase, 'ITcure': Italycure,
                   'FRcase': Francecase, 'FRcure': Francecure, 'SPcase': Spainacase, 'SPcure': Spaincure})


def M_Deaths(request):
    page = requests.get('https://www.worldometers.info/coronavirus/')

    soup = BeautifulSoup(page.content, 'html.parser')

    Location = []
    Victims = []
    df = pd.DataFrame(columns=["Location", "Victims"])

    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')
        Location.append(td[0].text)
        Victims.append(td[3].text)

    df = pd.DataFrame({'Location': Location, 'Victims': Victims})

    for k in range(len(Victims)):
        Victims[k] = Victims[k].translate({ord(','): None})
    Victims[7] = ''

    fig = go.Figure(data=go.Choropleth(
        locations=df['Location'],
        locationmode='country names',
        z=Victims,
        colorscale='Reds',
        marker_line_color='black',
        marker_line_width=0.5,
    ))
    fig.update_layout(
        title_text='Corona Virus (Total Deaths)',
        title_x=0.5,
        geo=dict(
            showframe=True,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    data = fig.show()

    return render(request, 'corona/index.html',
                  {'cases': cases, 'deaths': deaths, 'cured': cured, 'Sacase': Sacase, 'Sadeath': Sadeath,
                   'Sacure': Sacure, 'UScase': USAcase, 'UScure': USAcure, 'ITcase': Italycase, 'ITcure': Italycure,
                   'FRcase': Francecase, 'FRcure': Francecure, 'SPcase': Spainacase, 'SPcure': Spaincure})


def M_Recovered(request):
    page = requests.get('https://www.worldometers.info/coronavirus/')

    soup = BeautifulSoup(page.content, 'html.parser')

    Location = []
    Recovered = []

    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    for tr in table_rows:
        td = tr.find_all('td')
        Location.append(td[0].text)
        Recovered.append(td[5].text)

    df = pd.DataFrame({'Location': Location, 'Recovered': Recovered})

    for k in range(len(Recovered)):
        Recovered[k] = Recovered[k].translate({ord(','): None})

    Recovered[7] = ''

    fig = go.Figure(data=go.Choropleth(
        locations=df['Location'],
        locationmode='country names',
        z=Recovered,
        colorscale='Reds',
        marker_line_color='black',
        marker_line_width=0.5,
    ))
    fig.update_layout(
        title_text='Corona Virus (Recovered)',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    fig.show()
    return render(request, 'corona/index.html',
                  {'cases': cases, 'deaths': deaths, 'cured': cured, 'Sacase': Sacase, 'Sadeath': Sadeath,
                   'Sacure': Sacure, 'UScase': USAcase, 'UScure': USAcure, 'ITcase': Italycase, 'ITcure': Italycure,
                   'FRcase': Francecase, 'FRcure': Francecure, 'SPcase': Spainacase, 'SPcure': Spaincure})
