import pandas
import requests
import json
import ast
import numpy
from datetime import datetime
from tqdm import tqdm, tqdm_notebook
import statsmodels.formula.api as sm

issues_url = 'https://viewer.cdn.partica.online/viewer/sites/archive.nationalgeographic.com/url.json'

response = requests.get(issues_url)
json = response.json()
json = json['publications']
json = json[0]
json = str(json)[11:-862]

json = ast.literal_eval(json)
issues = pandas.DataFrame(json)
issues.to_csv('Downloads/NatGeo/issues.csv', index=False, encoding='utf-8-sig')

missingToc = []
missingFolios = []
allPages = []
issuesInfo = []

for index, row in tqdm(issues.iterrows(), total=issues.shape[0]):
    print('\nParsing {} Issue' .format(row['name']))
    issue_url = 'https://viewer.cdn.partica.online/viewer/' + row['path'] + '/replica.json'
    print(issue_url)
    response = requests.get(issue_url)
    json = response.json()
    allContent = []
    if 'toc' in json:
        for i in range(0, len(json['toc'])):
            content = json['toc'][i]
            content = pandas.DataFrame(content)
            allContent.append(content)
        allContent = pandas.concat(allContent, ignore_index=True)
        allContent['issue'] = row['path']
        allPages.append(allContent)
        print(allContent.shape)
        missToc = False
    else:
        print('No toc')
        missingToc.append(row['path'])
        missToc = True
    if 'folios' in json:
        folios = list(json['folios'])
        pages = []
        for i in folios:
            splitpages = i.split('-')
            pages.extend(splitpages)
        issueInfo = {'issue' : row['path'], 'numPages' : len(pages), 'numAds' : sum('A' in s for s in pages), 'Missing ToC' : missToc}
        issuesInfo.append(issueInfo)
    else:
        missingFolios.append(row['path'])

print('{} Issues Missing ToC' .format(len(missingToc))) #50 missing
print('{} Issues Missing Folios' .format(len(missingFolios))) #0 missing
allPages = pandas.concat(allPages)
issuesInfo = pandas.DataFrame(issuesInfo)
allPages.to_csv('Downloads/NatGeo/allPages.csv', index=False, encoding='utf-8-sig')
issuesInfo.to_csv('Downloads/NatGeo/issuesInfo.csv', index=False, encoding='utf-8-sig')

#Load issue info
issues = pandas.read_csv('Downloads/NatGeo/issues.csv')
issues['issueDate'] = pandas.to_datetime(issues['issueDate'], utc=False)
issuesInfo = pandas.read_csv('Downloads/NatGeo/issuesInfo.csv')
allIssues = pandas.merge(issues, issuesInfo, left_on='path', right_on='issue')

#Load article info
articles = pandas.read_csv('Downloads/NatGeo/allPages.csv')
articles = articles.loc[articles['section'] == 'Article'] #only desire searching through article metadata, not photos or department info
articles = articles.replace(numpy.nan, '', regex=True)
articles['textSearch'] = (articles['title'].map(str) + ' ' + articles['abstract']).str.strip() #combining title and abstract to form text field

#Load country info
countries = pandas.read_csv('Downloads/NatGeo/continentCountries.csv') #from https://datahub.io/JohnSnowLabs/country-and-continent-codes-list
countries['countryName'] = countries['Country_Name'].str.split(',').str[0] #removing wordy parts of country titles e.g. 'Afghanistan, Islamic Republic of' --> 'Afghanistan'
countries = countries.drop(columns=['Continent_Code', 'Two_Letter_Country_Code', 'Country_Number', 'Country_Name'])
countries = countries.rename(columns={"Continent_Name": "continentName"})
countries.loc[countries['countryName'] == 'Russian Federation', 'countryName'] = 'Russia' #renaming wordy countries
countries.loc[countries['countryName'] == 'United States Virgin Islands', 'countryName'] = 'Virgin Islands'
countries.loc[countries['countryName'] == 'United States of America', 'countryName'] = 'America'
countries.loc[countries['countryName'] == 'United Kingdom of Great Britain & Northern Ireland', 'countryName'] = 'United Kingdom'
countries.loc[countries['countryName'] == 'Syrian Arab Republic', 'countryName'] = 'Syria'
countries.loc[countries['countryName'] == 'Slovakia (Slovak Republic)', 'countryName'] = 'Slovakia'
countries.loc[countries['countryName'] == 'Sint Maarten (Netherlands)', 'countryName'] = 'Sint Maarten'
countries.loc[countries['countryName'] == 'CuraÃ§ao', 'countryName'] = 'Curacao'
countries.loc[countries['countryName'] == 'Libyan Arab Jamahiriya', 'countryName'] = 'Libya'
countries.loc[countries['countryName'] == "Lao People's Democratic Republic", 'countryName'] = 'Laos'
countries.loc[countries['countryName'] == 'Kyrgyz Republic', 'countryName'] = 'Kyrgyzstan'
countries.loc[countries['countryName'] == 'Holy See (Vatican City State)', 'countryName'] = 'Vatican City'
countries.loc[countries['countryName'] == 'Palestinian Territory', 'countryName'] = 'Palestine'
countries.loc[countries['countryName'] == 'Ã…land Islands', 'countryName'] = 'Aland Islands'
countries.loc[countries['countryName'] == 'Falkland Islands (Malvinas)', 'countryName'] = 'Falkland Islands'
countries.loc[countries['countryName'] == 'Cocos (Keeling) Islands', 'countryName'] = 'Cocos Islands'
countries.loc[countries['countryName'] == 'Brunei Darussalam', 'countryName'] = 'Brunei'
countries.loc[countries['countryName'] == 'Bouvet Island (Bouvetoya)', 'countryName'] = 'Bouvet Island'
countries.loc[countries['countryName'] == 'Antarctica (the territory South of 60 deg S)', 'countryName'] = 'Antarctica'
countries = countries.append(pandas.DataFrame([['Europe', 'GBR', 'England']], columns=countries.columns)) #adding more specific country titles/alternatives
countries = countries.append(pandas.DataFrame([['Europe', 'GBR', 'Wales']], columns=countries.columns))
countries = countries.append(pandas.DataFrame([['Europe', 'GBR', 'Scotland']], columns=countries.columns))
countries = countries.append(pandas.DataFrame([['Europe', 'GBR', 'Britain']], columns=countries.columns))
countries = countries.append(pandas.DataFrame([['North America', 'USA', 'USA']], columns=countries.columns))
countries = countries.append(pandas.DataFrame([['Europe', 'CZE', 'Czechia']], columns=countries.columns))
countries = countries.append(pandas.DataFrame([['Africa', 'CIV', 'Ivory Coast']], columns=countries.columns))
countries = countries[countries.Three_Letter_Country_Code != 'PRK'] #impossible to dedupe North/South Korea and the two Congo's
countries = countries[countries.Three_Letter_Country_Code != 'COD']

#tagging each article text with one or more countries (if applicable)
extraction = (
    articles['textSearch'].str.extractall(f"({'|'.join(countries['countryName'])})")
        .rename(columns={0: 'countryName'})
)

tagged = extraction.droplevel(1).join(articles).reset_index(drop=True)
tagged = tagged.drop(columns=[1])

tagged.to_csv('Downloads/NatGeo/taggedCountries.csv', index=False, encoding='utf-8-sig')
tagged = pandas.read_csv('Downloads/NatGeo/taggedCountries.csv')

tagged = tagged.drop_duplicates(['id', 'countryName']) #removing duplicates that are tagged because they reference country's name > 1 time in textSearch
realGeorgia = ['528313f1-95d1-4d6c-b386-2cdd4332dcfb', 'b824eb9e-3e69-45e9-948c-9e8d58050e4d', 'b0077b66-48a9-4c3c-94ef-351bf7866650', '316028e8-47bb-4a36-b746-79a7c6e19b00', '9bb0bc49-b503-4a94-8420-ee1d30f3867e']
realJersey = ['fbc03bf5-9fb7-4b98-81bc-0afc79d5624e'] #manually selecting only Georgia, Jersey, India country info, not states/native americans/etc.
realIndia = ['005ed5f7-7124-40ff-8d11-884acbf8d603', '014d26dc-8808-47e2-91a7-cc2283ebbc08', '01a89161-60cd-416c-ac13-c0815d6f6ee6', '01f24de7-84b1-4173-b948-6339bcddea16', '02d50a61-f6c5-4d1b-bd6d-ee005775d985', '08667edb-e999-4186-a3d8-48bf63444913', '0933ed2f-5005-478e-805a-49aff4995855', '0a010bf1-af15-478e-a176-8641edc7977e', '0d89d4f7-c89e-4d69-83f1-b81fef2e1d95', '0e03877f-0c46-424f-ad74-0f659509f77d', '0ee7f5ee-e06f-4856-a387-8afc97876d42', '1430946e-8831-4f1c-995f-ad24fb48c273', '147851a8-9e10-49be-9c46-1c184e699fd4', '155388ef-6bc8-49d0-a41b-17bad6478d76', '1854eda9-ce72-4403-9627-b94c65e4c78d', '25e0b34e-18e0-44e7-a73d-eedaa37cc7c6', '2a27b990-a194-447b-94e0-2c80944ff66b', '2f2d3a09-cda8-4e9a-86cb-0de600c8dfb8', '315cea60-7382-4019-a3e0-801adc58b23d', '31bf0551-33c2-46ca-a144-5235b0a2ef21', '31da0a57-e989-4dd6-980c-fadd66df79e7', '31f2edb6-eccb-40b8-ade1-39487b4d4b61', '336b73dc-ca1a-4527-a4df-16f81120c594', '3402181b-ca59-4128-bf27-13c558003906', '353415c0-819a-45d2-bcc5-bf264b982b61', '370b9d08-06e9-4427-9f0d-2113853a431e', '3aa4e9b7-82b1-4ff4-a7bd-071c31abdecb', '3bb9e901-5aeb-4e50-805e-76c947b53fb2', '3d22e7ae-6d21-406d-8e0d-3c1f8624e89e', '3e5c5ab2-c104-4c3f-8b52-da056454e6b6', '425d3f0c-dfb1-422d-846c-4eba4071a755', '45d0dc09-6454-4633-b44c-df5f5128c9f3', '49d2b744-a765-432b-a778-b690ead0170a', '4ae1cfa2-c54f-4330-b6aa-1a19338faef6', '4dcd835f-f4a2-474c-82be-2d11eaf33456', '4df55edc-6de1-4cda-9bb7-bf016c05b0ff', '4f262bac-058f-4e39-bd3e-bfd831419741', '50799f23-fbc4-4d08-84ad-6f7b9ea90edd', '51cc3b96-7411-489b-a231-ebeff89cb21a', '52fef335-fc94-4bc2-a25e-cdca8baf199f', '54a66758-0422-45c8-99f5-8dfe062d881b', '54f87c01-8f66-4a13-b019-ecf424ef32ac', '572a3b5f-1105-4c9d-b4be-1cc34c1e2bed', '5bdcdcc2-7409-4dff-89f7-4487047d4f40', '5ebd70a1-e72a-4a37-aa79-e36efa1dd2ff', '5fd7beec-f4b6-477c-8c7b-ed51b2ebfeb5', '648db7a9-21d5-4ee4-9e0a-22118ab9f6c9', '664d6932-6d4f-476a-b752-71a15258e729', '68cd69d1-9d6d-440a-aaa4-a1c081f96585', '6afeeaf7-83cb-4d4e-a78f-24d5d79a6fe7', '70de5007-1a73-4161-b81b-76ade6153130', '70fd2920-4130-49b3-8d8e-1de530d92d46', '717db1c4-7a0e-4c22-8ef5-12b477345c60', '72c5e54e-e5d3-47b0-8faa-e9cddb660da4', '73fd23d8-08ce-4f4d-92e8-6fb92f824047', '745c1d92-b77e-4575-bae7-2ceaa16d7785', '7494acb5-290d-49d9-8198-81055115fb18', '7532e500-20bd-44f4-b2bf-d4c0868d0340', '780397d2-ebf4-44bc-8586-6f233cf4f7e9', '78a9f370-35da-4b84-ba4b-cc5f53df4483', '7b701036-4c39-4334-bb59-541f278bd87d', '7cc19dd5-d45d-43b7-a486-5393c3a4c42b', '7dd45afb-b3d2-4042-9c7c-cf17ea08677a', '800a274a-595f-4f42-af1f-ed1baf8f9261', '814907f6-b400-46f6-a0b6-e72e09e4cefe', '83d9caa8-18e4-478c-a505-c65eb893e5fe', '84c3257d-fea8-4daf-bcee-ef9677e0e936', '85ef1cd1-ff6c-48e0-9396-884cc9191ef0', '860dc682-0793-4cfe-9889-db0398ede5ee', '8bb3ef9e-926b-4795-8f84-3f26f2bc212a', '8cfd5180-bb30-4525-9eec-44833bc80632', '8d90f56f-06ea-4919-b24d-290071a6f910', '910301bb-c32c-4f54-9bf3-c8a4a69c7558', '9564c624-66ce-4b17-837f-f85f24da48f1', '964ecb60-afe3-47b9-989a-3eef5e27d471', '99286fa1-f7db-4643-b6f3-2bf9d17144db', '9a92b8f4-9648-48fe-84fb-0a356cf873f6', '9aee4480-6752-4574-854a-7847ab49dc10', '9cbb0a7e-342d-4030-8cb5-95922832279e', '9cc03073-6c09-449a-a2ae-940272d8e0ac', '9da28b01-89cb-437e-9515-487e6af185b0', 'a334ebcf-7c31-46a0-9b1f-703d51aa6c64', 'a988eb6d-ff72-4f03-8646-8b35b05e3f81', 'b15621f0-8ee7-4983-b269-594b02c22ba1', 'b1590dcb-22bb-48f1-9a7b-1f0648f5511f', 'b267e003-bcfe-4075-a220-21181f3a88b3', 'b50acc9a-94e3-4b86-acbc-3b474032c563', 'b583b8c2-44f2-4965-952a-98f353cd7e0b', 'b5b66934-2e00-428c-a71f-48a7a06bfd38', 'b91a742f-2f8e-46e2-9d88-3d077213ed3c', 'b9634068-d94d-403d-800d-322c2cecf89a', 'b99079a6-e2ba-4eb5-a64a-c7696d609ac4', 'ba93b4d6-57dd-4af9-a0a8-b6d195ea19db', 'bad95194-f9f8-4b9e-88bf-60201ae80598', 'c500fff5-8111-46af-aa67-253b025ef978', 'c95b72c9-931b-432c-a373-f2c2af4a92d8', 'caabcb7b-3f4d-42c9-a646-00e3dd61979e', 'cc4258cb-e373-43db-8311-36b9a9f6a43a', 'cf424e33-7efc-4855-9824-d01d677aee83', 'd09c4561-7d1c-4b9d-af81-4067793b9b1e', 'd916d006-a230-4d1b-adaa-f55c64e9b9d5', 'daaae818-b808-4216-9cd6-c4f0f83ab13d', 'dbccf9ae-1d3e-4c54-b43b-25839ada7219', 'e0c2ec05-4a46-4fd0-aebd-42f2648600ee', 'e13fe5f5-6b5c-4548-9ce9-d7602d79ce26', 'e166222e-4c5b-4f0b-882e-86f2d9f89f35', 'e18ccfcf-99c8-4ff9-9785-3545c64ef905', 'e35e1478-f4e6-4f26-b1cb-bd2c8a1830e0', 'e39b268c-b16c-433a-bec0-ca1f7ffe541e', 'e4403f0e-e095-47d4-8bec-038cc739c012', 'e5066275-7451-4d75-bc13-4e97f0a5279d', 'e94cab96-c413-48da-a3f7-db979d80f3da', 'ec923226-e278-4b62-a3f8-35d9fca59fdb', 'ecd89243-d26b-4b1a-a554-a873e541413c', 'f774a039-47b2-4627-ad9d-5226b4151ffa', 'fdf58b3c-a624-46a0-9cc0-97ff7db15b60']
realNigeria = ['9244dae9-4247-4250-a265-03ae12b24276', '59ec6d7d-7761-44d2-afd9-9e05ad4f02b4', '611ae471-ef8d-4e36-858d-ff00c4fa4a90', '94681668-1c5e-4c58-ab05-a8f7b13d1b11', '52187b78-120b-4089-927b-5d79bd0539e0', 'a0afa27e-2cf2-4fc0-87af-e9a3217953f3', 'bacaa47c-34c8-4090-808e-61048e3457fa', '927864b2-4fdb-4c9f-8b79-332bb90439ac', '79c92543-fe27-46e9-9e28-180f9cf7f66c', '71e7246b-2129-49be-a0c6-e6a84e338bbc']
realDominicanRepublic = ['ad043be3-5ce1-4ca8-bb61-6e5b75d1328a', '3eacaa0a-bae7-474e-ad1c-cafcdcb20aaa', 'd3643426-1e55-47ac-9f5c-9acfb1dfaa0f', '41a12838-8e07-4bef-8ed4-2c975f9037f8']
realGuinea = ['bcb50fd6-aa62-42b2-8584-e4cb6237a806']
realNetherlandsAntilles = ['8dda10f7-b78d-48df-81c7-9461ded3e266']
realChad = ['fc80c5c8-db48-4358-8990-a7b873352e2f', '72cdf759-7ce8-47a2-81db-23fda85310a0', 'bacaa47c-34c8-4090-808e-61048e3457fa']
tagged = tagged.loc[((tagged['id'].isin(realGeorgia)) & (tagged['countryName'] == 'Georgia')) | (tagged['countryName'] != 'Georgia')]
tagged = tagged.loc[((tagged['id'].isin(realJersey)) & (tagged['countryName'] == 'Jersey')) | (tagged['countryName'] != 'Jersey')]
tagged = tagged.loc[((tagged['id'].isin(realIndia)) & (tagged['countryName'] == 'India')) | (tagged['countryName'] != 'India')]
tagged = tagged.loc[((tagged['id'].isin(realChad)) & (tagged['countryName'] == 'Chad')) | (tagged['countryName'] != 'Chad')]
tagged.loc[(tagged['id'].isin(realNigeria)) & (tagged['countryName'] == 'Niger'), 'countryName'] = 'Nigeria'
tagged.loc[(tagged['id'].isin(realDominicanRepublic)) & (tagged['countryName'] == 'Dominica'), 'countryName'] = 'Dominican Republic'
tagged.loc[(~tagged['id'].isin(realGuinea)) & (tagged['countryName'] == 'Guinea'), 'countryName'] = 'Papua New Guinea'
tagged.loc[(tagged['id'].isin(realNetherlandsAntilles)) & (tagged['countryName'] == 'Netherlands'), 'countryName'] = 'Netherlands Antilles'

#compare continents over time
result = pandas.merge(tagged, countries, on='countryName') #more rows added due to multiple continents per country
result = pandas.merge(result, allIssues, left_on='issue', right_on='path')
result.to_csv('Downloads/NatGeo/resultNatGeo.csv', index=False, encoding='utf-8-sig')

#condense into continents, analyze by year
result = pandas.read_csv('Downloads/NatGeo/resultNatGeo.csv')
result['year'] = pandas.DatetimeIndex(result['issueDate']).year
result = result.loc[result['Three_Letter_Country_Code'] != 'USA'] #remove America bc/ of shaky matching to all 'America's'
continents = result.pivot_table(index='year', columns='continentName', values='path', aggfunc=len, fill_value=0)
continents.reset_index(level=0, inplace=True)
continents.to_csv('Downloads/NatGeo/continentReferences.csv')
#Plotting continents in Tableau occurs now

#Load world population
pop = pandas.read_csv('Downloads/NatGeo/worldPopulation.csv') #https://datahub.io/JohnSnowLabs/population-figures-by-country
pop = pop[['Country_Code', 'Year_2016']]
pop = pandas.merge(countries.drop_duplicates(['Three_Letter_Country_Code']), pop, left_on='Three_Letter_Country_Code', right_on='Country_Code', how='left')
pop = pop[['Three_Letter_Country_Code', 'Year_2016']]
pop.columns = ['countryCode', 'population']
pop = pop.replace(numpy.nan, 0)
pop = pop.loc[pop['countryCode'] != 0]
pop.loc[pop['countryCode'] == 'ERI', 'population'] = 5750433 #Eritrea missing population, what other countries are missing?

#Merge with counts of reference numbers for each country
condensed = result.drop_duplicates(['id', 'countryName']) #remove duplicates due to countries having >1 continent
condensed = condensed.groupby(['Three_Letter_Country_Code'])['countryName'].count()
condensed = pandas.DataFrame(condensed)
condensed.reset_index(level=0, inplace=True)
condensed.columns = ['countryCode', 'numReferences']
condensed = pandas.merge(pop, condensed, on='countryCode', how='left') #left-joining to keep countries that are not referenced at all
condensed = condensed.replace(numpy.nan, 0)
condensed = condensed.sort_values(by=['numReferences'])
condensed.to_csv('Downloads/NatGeo/countryReferences.csv')
#Plotting countries in Tableau occurs now

#For modeling purposes, remove USA and other countries due to extraneous factors
countryComparisons = condensed.loc[condensed['countryCode'] != 'USA']
countryComparisons = condensed.loc[condensed['countryCode'] != 'PRK']
countryComparisons = condensed.loc[condensed['countryCode'] != 'KOR']
countryComparisons = condensed.loc[condensed['countryCode'] != 'COD']
countryComparisons = condensed.loc[condensed['countryCode'] != 'COG']
countryComparisons.sort_values(by=['numReferences'])
model = sm.ols(formula="numReferences ~ population", data=countryComparisons).fit()
print(model.summary())

countryComparisons['predictedReferences'] = model.predict()
countryComparisons['residualReferences'] = countryComparisons['numReferences'] - countryComparisons['predictedReferences']
countryComparisons['residualReferencesPct'] = countryComparisons['numReferences'] / countryComparisons['predictedReferences']
print(countryComparisons.sort_values(by=['residualReferencesPct', 'residualReferences']).to_string())