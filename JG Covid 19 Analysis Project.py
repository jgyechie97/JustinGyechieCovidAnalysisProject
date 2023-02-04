##Covid-19 Data Analysis with Python
'''The outbreak of Covid-19 resulted in a lot of restrictions which resulted in so many impacts on the global economy. Almost all the countries were impacted negatively by the rise in the cases of Covid-19.
We want to analyse the spread of Covid-19 and the impacts of Covid-19 on the economy
the data set contains data about:
the country code
name of all the countries
date of the record
Human development index of all the countries
Daily covid-19 cases
Daily deaths due to covid-19
stringency index of the countries
the population of the countries
GDP per capita of the countries'''


#Import the necessary Python libraries and datasets
import pandas as pd
import plotly.express as px


data = pd.read_csv(r"C:\Users\justi\OneDrive\Documents\Data Analysis Projects\raw_covid19_data.csv", parse_dates=["date"])
data2 = pd.read_csv(r"C:\Users\justi\OneDrive\Documents\Data Analysis Projects\transformed_covid19_data.csv", parse_dates=["DATE"])
print(data)



'''r" = the string will be treated as raw string. This enables the backslashes (\) to be treated as literal characters.
this is useful for when you deal with strings that have many backslashes, e.g. regular expressions or directory paths on Windows.

parse_date parameter convinces pandas to turn things into real daterime types
because by default, data columns are re[resemted as object when loading data from a CSV file.
to read the date column correctcly, we use the arguement parse_dates to specify a list of date columns
make sure to use the exact same used in the raw data file e.g column 1 ="DATE" so parse ="DATE" or column 2 ="date" so parse ="date

The data we are using contains the data on covid-19 cases and their impact on GDP from December 31, 2019, to October 10, 2020.

The dataset that we are using here contains two data files. One file contains raw data, and the other file contains transformed one. 
But we have to use both datasets for this task, as both of them contain equally important information in different columns. ##
So let’s have a look at both the datasets one by one:'''


##first dataset
print(data.head())

##second dataset
print(data2.head())

##we have to combine both datasets by creating a new dataset.
##But before we create a new dataset, let’s have a look at how many samples of each country are present in the dataset:
data2["COUNTRY"].value_counts()


##So we don’t have an equal number of samples of each country in the dataset. Let’s have a look at the mode value: (mode - number that appears the most)
data2["COUNTRY"].value_counts().mode()

##so we can see the mode value is 294.
##we will use this to divided the sum of all the samples related to human development index, GDP per capita & population

##Lets create a new dataset by combining the necessary columns from both datasets
##we first aggreate the data (aggregating data = combining individual-level data to produce a summary form)

code = data2["CODE"].unique().tolist()
##tolist() converts a given array to an ordinary list with the same items, elements, or values.
##np.array() converts a list to array
country = data2["COUNTRY"].unique().tolist()
hdi = []
tc = []
td = []
sti = []
population = data2["POP"].unique().tolist()
gdp = []

for i in country:
    hdi.append((data2.loc[data2["COUNTRY"] == i, "HDI"]).sum() / 294)
    tc.append((data.loc[data["location"] == i, "total_cases"]).sum())
    td.append((data.loc[data["location"] == i, "total_deaths"]).sum())
    sti.append((data2.loc[data2["COUNTRY"] == i, "STI"]).sum() / 294)
    population.append((data.loc[data["location"] == i, "population"]).sum() / 294)

##Pandas provide a unique method to retrieve rows from a Data frame. DataFrame.loc[] method is a method that takes only index labels and retur

##If you are trying to create a dataframe from the extracted values then, you need to store them in list before performing zip
##e.g.
# List1
##Name = ['tom', 'krish', 'nick', 'juli']

# List2
##Age = [25, 30, 26, 22]

##Above two lists can be merged by using list(zip()) function. Now, create the pandas DataFrame by calling pd.DataFrame() function.

##zip can be used to map values
##e.g.
## names = ['Mukesh', 'Roni', 'Chari']
## ages = [24, 50, 18]

##for i, (name, age) in enumerate(zip(names, ages)):
##print(i, name, age)
##this would map Mukesh = 24, Roni = 50, Chari = 18

aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)),
                               columns=["Country Code", "Country", "HDI",
                                        "Total Cases", "Total Deaths",
                                        "Stringency Index", "Population"])
print(aggregated_data.head())

#GDP per capita is not included because don't have the correct figure in dataset.

#Instead we can create a subsample from this dataset due to having so many different countries in this data.

#To create a subsample from this dataset, we will select the top 10 countries with the highest number of coviid-19 cases.
# This is a perfect sa,ple to study the economic impacts of covid 19

#We start by sporting the dat according to total case:

##print(aggregated_data)

#df2=aggregated_data.sort_values('Total Cases', ascending=False)
#print(df2)

tcdata = aggregated_data.sort_values(by=["Total Cases"], ascending=False)
print(tcdata.head())

#Select the top 10 countries with the highest number of cases:
tcdata = tcdata.head(10)
print(tcdata)

#Now add in two more columns (GDP per capita before Covid 19, GDP per capita during Covid-19) to the dataset:

tcdata["GDP Before Covid"] = [65279.53, 8897.49, 2100.75,
                            11497.65, 7027.61, 9946.03,
                            29564.74, 6001.40, 6424.98, 42354.41]

tcdata["GDP After Covid"] = [63543.58, 6796.84, 1900.71,
                            10126.72, 6126.87, 8346.70,
                            27057.16, 5090.72, 5332.77, 40284.64]

print(tcdata)

##this gdp data is collected maunally based on the new dataframe of the top 10 countries with most coivd cases.

#Analyzing the spread of Covid-19
#Start by analysing the countries with the highest cases of covid

##using the plotly express libary we can create a easy bar chart

figure1 = px.bar(tcdata, y='Total Cases', x='Country',
                 title="Countries with Highest Covid Cases", width=600, height=400)
figure1.show()

#14,6

##countries with higest deaths

figure2 = px.bar(tcdata, y='Total Deaths', x='Country',
                 title="Countries with Highest Deaths", width=600, height=400)
figure2.show()

print(tcdata)

tcdata.get('Country')

##print(tcdata["Country"])
##Compare the total number of cases and total deaths

import plotly.graph_objs as go

fig = go.Figure()
fig.add_trace(go.Bar(
    x=tcdata["Country"],
    y=tcdata["Total Cases"],
    name='Total Cases',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=tcdata["Country"],
    y=tcdata["Total Deaths"],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45, width=800, height=600)
fig.show()

##except KeyError as err: 'Country'

# Percentage of Total Cases and Deaths
cases = tcdata["Total Cases"].sum()
deceased = tcdata["Total Deaths"].sum()

labels = ["Total Cases", "Total Deaths"]
values = [cases, deceased]

#print(labels)
#print(values)
#px is ploty as express
fig = px.pie(tcdata, values=values, names=labels,
             title='Percentage of Total Cases and Deaths', hole=0.6)
fig.show()

#Below is how you can calculate the death rate of Covid-19 cases:
death_rate=(tcdata["Total Deaths"].sum()/tcdata["Total Cases"].sum())*100
print("Death Rate = ", death_rate)


#Another important column in this dataset is the stringency index.
#It is a composite measure of response indicators, including school closures, workplace closures, and travel bans.
#It shows how strictly countries are following these measures to control the spread of covid-19:
fig = px.bar(tcdata, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='Stringency Index', height=400,
             title= "Stringency Index during Covid-19")
fig.show()

#Here we can see that India is performing well in the stringency index during the outbreak of covid-19.

#Analyzing Covid-19 Impacts on Economy
#Here the GDP per capita is the primary factor for analyzing the economic slowdowns caused due to the outbreak of covid-19.
#look at the GDP per capita before the outbreak of covid-19 among the countries with the highest number of covid-19 cases:

fig = px.bar(tcdata, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='GDP Before Covid', height=400,
             title= "GDP Per Capita Before Covid-19")
fig.show()

#gdp before is in dataframe

fig = px.bar(tcdata, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='GDP After Covid', height=400,
             title= "GDP Per Capita After Covid-19")
fig.show()


#Compare before and after effects on GDP per capita from Covid

import plotly.graph_objs as go
fig = go.Figure()
fig.add_trace(go.Bar(
    x=tcdata["Country"],
    y=tcdata["GDP Before Covid"],
    name='GDP Per Capita Before Covid-19',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=tcdata["Country"],
    y=tcdata["GDP After Covid"],
    name='GDP Per Capita After Covid-19',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45, width=800, height=600, xaxis_title='Country', yaxis_title='GDP Per Capita')
fig.show()


#You can see a drop in GDP per capita in all the countries with the highest number of covid-19 cases.

#One other important economic factor is Human Development Index.
#It is a statistic composite index of life expectancy, education, and per capita indicators.
fig = px.bar(tcdata, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='HDI', height=400,
             title= "Human Development Index during Covid-19")
fig.show()



