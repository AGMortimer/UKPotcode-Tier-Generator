import requests
import pandas as pd
from bs4 import BeautifulSoup

data = pd.read_excel('Postcodes.xlsx',index_col = 'user_id')


current_tier_level = []
new_tier_level = []
new_tier_level_from_date = []


for postcode in data['postalcode']:
    postcode = postcode.replace(' ','')
    URL = 'https://www.gov.uk/find-coronavirus-local-restrictions?postcode='+postcode
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    	
    	#current tier classification
    tier = soup.find_all('title')
    tier_change = soup.find_all('p', 'govuk-body')
    from_change = soup.find_all('h2')
    
    no_info = '[<title>There is no information about the restrictions in this area - GOV.UK</title>]'
    #Non-existant postcode
    if str(tier) == no_info:
        result_current = 'Invalid Postcode'
        result_next = 'N/A'
        result_fromnext = 'N/A'   
    #Scotlandd and wales postcodes
    elif len(tier_change) >= 3:
        if str(tier_change[2]).split()[-2][:-1] in ('Wales','Scotland'):
            result_current = str(tier_change[2]).split()[-2][:-1]
            result_next = 'N/A'
            result_fromnext = 'N/A'  

    #english postcodes, check if changing, then what's left   
        else:#(not str(tier_change[2]).split()[-2][:-1] == 'Wales') and (not str(tier_change[2]).split()[-2][:-1] == 'Scotland'):
            if str(tier) == '[<title>The tier for this area is changing soon - GOV.UK</title>]':
                moment_tier = str(tier_change[2]).split()[-2][0]
                
                bookmark = str(tier_change[3]).split().index('Tier')
                next_tier = str(tier_change[3]).split()[bookmark+1][0]
                
                from_tier = str(from_change[2]).split()[-2]+' '+str(from_change[2]).split()[-1][:3]
                
                result_current = moment_tier
                result_next = next_tier
                result_fromnext = from_tier
    			
            else:
                result = str(tier[0])
                result = result.split()
                result_current = result[6][0]
                result_next = 'N/A'
                result_fromnext = 'N/A'      
                
                
    else:#(not str(tier_change[2]).split()[-2][:-1] == 'Wales') and (not str(tier_change[2]).split()[-2][:-1] == 'Scotland'):
        if str(tier) == '[<title>The tier for this area is changing soon - GOV.UK</title>]':
            moment_tier = str(tier_change[2]).split()[-2][0]
                
            bookmark = str(tier_change[3]).split().index('Tier')
            next_tier = str(tier_change[3]).split()[bookmark+1][0]
                
            from_tier = str(from_change[2]).split()[-2]+' '+str(from_change[2]).split()[-1][:3]
                
            result_current = moment_tier
            result_next = next_tier
            result_fromnext = from_tier
    			
        else:
            result = str(tier[0])
            result = result.split()
            result_current = result[6][0]
            result_next = 'N/A'
            result_fromnext = 'N/A'    
     	
    
    
    if result_current in ('1','2','3','4','Wales','Scotland'):
        current_tier_level.append(result_current)
    else:
        current_tier_level.append('ERROR')
        
    
    if result_next in ('1','2','3','4','N/A'):
        new_tier_level.append(result_next)
    else:
        new_tier_level.append('ERROR')
        
        
    new_tier_level_from_date.append(result_fromnext)


data['Current Tier Level'] = current_tier_level
data['New Tier Level'] = new_tier_level
data['New Tier Level From Date'] = new_tier_level_from_date


data.to_excel("Postcodes - with tiers.xlsx")
