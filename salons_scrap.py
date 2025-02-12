import time
import requests
import pandas as pd
import json
import os

HEADERS = {
    "Cookie": '''QuantumMetricUserID=b193de7a702ea31c7992591895da2363; s_fid=67D81E4F99537405-10EC592C26A802C0; rxVisitor=17392591203047QN7Q7GD10M5U99PSIS4LUOIK3H2KDR5; _gcl_au=1.1.979278188.1739259125; s_ecid=MCMID%7C28614217048021289851963175683140868194; __tvpa=22c931a3f078d38e8a78d88dce8d0639; _scid=ghmZikNZuMQXESLDjAjB7HkuVQZDdei9; _caid=57b153d1-f493-4494-9906-94a63261c146; _fbp=fb.1.1739259312021.312852665719427203; _tt_enable_cookie=1; _ttp=6GlUnTLDc2SN3RNkVadDY3T6FL-.tt.1; _ScCbts=%5B%5D; _pin_unauth=dWlkPU0yUXpaRGMyTXpBdFlUaGpPUzAwWkdJMExXSmxOR1F0WmpSak1tRXhORGRtWm1Saw; _sctr=1%7C1739214000000; BELLA_REMEMBER_ME=true; __gads=ID=96677f85cc2f11db:T=1739259121:RT=1739260132:S=ALNI_MYav-yJv0kXy3r-UmF7UlVabmjO1g; __gpi=UID=00000fe36f9c3074:T=1739259121:RT=1739260132:S=ALNI_MZFaazIQVH7TGFUnQt8_kolRes6QQ; __eoi=ID=223dd917e7b52aa2:T=1739259121:RT=1739260132:S=AA-AfjYxczT-k6EcJyOSgvSwYbH3; _rdt_uuid=1739259309694.1365b986-07de-46a1-8c1d-744a89613aa1; _rdt_em=3c010e52ef16c7ba1833f047620363a56abe3a830278bab612fba18782f6e6cb; _scid_r=kZmZikNZuMQXESLDjAjB7HkuVQZDdei9R_DeIQ; _derived_epik=dj0yJnU9VjJrczkwd3pkSUlyeXhILXVBRHc2TjJtUDRWX1VNajImbj0yaWh3RFhNcU83Y1ptS0ZaUVJxc25nJm09MSZ0PUFBQUFBR2VyQU9VJnJtPTEmcnQ9QUFBQUFHZXJBT1Umc3A9NQ; s_nr=1739260136549-New; ABTasty=uid=2g3f0r93b2rd253j&fst=1739259126748&pst=-1&cst=1739259126748&ns=1&pvt=12&pvis=12&th=1051085.1305480.2.2.1.1.1739259436144.1739259602027.1.1_1314523.1629097.12.12.1.1.1739259126813.1739260137782.0.1; RT="z=1&dm=ulta.com&si=23dc39c6-96a9-4234-a81a-5b05f767879a&ss=m7062y3f&sl=b&tt=b87&obo=a&rl=1&ld=13vhn&r=210klr6h&hd=13vho"; dtSa=-; dtPC=-60$550263236_129h6vKACPDFOHPWGKUUPPPMBUOHHRVHLRWMIM-0e0; dtCookie=v_4_srv_20_sn_R6OA9Q7PODHAV7PF4CM36J7BIG414QG3_perc_100000_ol_0_mul_1_app-3Aaef46558697bc6fc_0_rcs-3Acss_0; rxvt=1739352064362|1739350263240; AMCVS_C218F16F55CC57607F000101%40AdobeOrg=1; s_cc=true; _gid=GA1.2.1829172693.1739350267; s_vi=[CS]v1|33D63E69DE64510C-4000077C41D2A802[CE]; AMCV_C218F16F55CC57607F000101%40AdobeOrg=1176715910%7CMCIDTS%7C20131%7CMCMID%7C28614217048021289851963175683140868194%7CMCAAMLH-1739964380%7C3%7CMCAAMB-1739964380%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739366780s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.4.0; _ga=GA1.2.1825889827.1739259126; QuantumMetricSessionID=cdc3b764f909481255f9e2c23b5e5cfb; refreshToken=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ODRiMGVhLWUyMWMtNGQyMi04MGFmLTQ1MWRiM2QzYmNkZCIsInBob25lTnVtYmVyIjoiKzEgOTE5LTM3NC0wMjExIiwiZmlyc3ROYW1lIjoiTXVoYW1tYWQiLCJsYXN0TmFtZSI6IlJhemEiLCJpYXQiOjE3MzkzNjQ5ODIuMjYxLCJleHAiOjE3NDQ1NDg5ODIsImp0aSI6IjVhMmRkNjkxLWMzM2UtNGUwZC1hMTQ5LTgyMWZiMWI5MDc5MCJ9.FfW681tzXFRrSYpSJXt5ahQsmAdbj9pQSXifaMQH6HgpTv5F5jFnvCh8tttoDcnfGlNYAQ5KJVAXlEP8EA92yQ; jwt=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ODRiMGVhLWUyMWMtNGQyMi04MGFmLTQ1MWRiM2QzYmNkZCIsInBob25lTnVtYmVyIjoiKzEgOTE5LTM3NC0wMjExIiwiZmlyc3ROYW1lIjoiTXVoYW1tYWQiLCJsYXN0TmFtZSI6IlJhemEiLCJpYXQiOjE3MzkzNjQ5ODIuMjYxLCJleHAiOjE3MzkzNjY3ODIsImp0aSI6Ijc2NDg1OTFkLWMwYTktNDI0YS04MTNiLTM5YzVkNzc4YzY1OSJ9.e3KAbBuFWvat9okKIRlH0fuXJOKhdLDBbelVgLPLhXZ5tQV4-V81UVY6nHNVrXGzVbDAWw147Ole1l7UtIHhrA; _ga_LKM7RC8LP8=GS1.1.1739364983.5.0.1739364983.60.0.0; utag_main=v_id:0194f3eb124300201459cdf014ac0506f002506700918$_sn:4$_se:1$_ss:1$_st:1739366787272$vapi_domain:ulta.com$ses_id:1739364987272%3Bexp-session$_pn:1%3Bexp-session; s_sq=ultaqa2%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fbeautyservices.ulta.com%25252Fstore%25252Fselection%2526link%253DSELECT%252520STYLIST%2526region%253Droot%2526.activitymap%2526.a%2526.c'''
}

STYLIST_BASE_URL = 'https://beautyservices.ulta.com/api/stylist/v2/location'



def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True


def get_salons(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    locations = data['results']['locations']

    
    for location in locations:
        
        
        locationID = location.get('locationID', '')
        name = location.get('name', '')  
        phone = location.get('phoneNumber', '')
        address = location.get('addressLine1', '')
        city = location.get('addressCity', '')
        state = location.get('addressState', '')
        zipCode = location.get('addressZip', '')
        country = location.get('addressCountry', '')
        categories = location.get('categories', [])
        
        hairStyling, curls, hairTreatments = False, False, False
        
        for category in categories:
            if category.get('name') == 'Hair Styling' and category.get('available', False):
                hairStyling = True
                
            if category.get('name') == 'Curls, Coils & Waves' and category.get('available', False):
                curls = True
                
            if category.get('name') == 'Hair Treatments' and category.get('available', False):
                hairTreatments = True

        try:
            stylist_response = requests.get(f'{STYLIST_BASE_URL}/{locationID}/fetchStylist', headers=HEADERS)
            stylist_response.raise_for_status()  
            stylist_data = stylist_response.json()
            stylist_count=0
            stylist_having_curls=0
            # each dict have a specializiation field if that contains stylist text then we can count that stylist
            for stylist in stylist_data:
                if 'specialization' in stylist and "Stylist" in stylist['specialization']:
                    stylist_count+=1
                if 'categories' in stylist:
                    for category in stylist['categories']:
                        if category.get('name') == 'Curls, Coils & Waves':
                            stylist_having_curls+=1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stylist data for location {locationID}: {e}")
            stylist_data = {}
        
        location_data = {
            'location ID': locationID,
            'Store Name': name,
            'Phone': phone,
            'Address': address,
            'City': city,
            'State': state,
            'Zip code': zipCode,
            'Country': country,
            'Offers Hair Styling': "True" if hairStyling else "False",
            'Offers Curls, Coils & Waves': "True" if curls else "False",
            'Offers Hair Treatments': "True" if hairTreatments else "False",
            'No of Stylists': stylist_count,
            'No of Stylist offering Curls, Coils & Waves': stylist_having_curls
        }
        
        print(location_data)
        appendProduct('ulta-salons.csv', location_data)
        time.sleep(1)

if __name__ == '__main__':
    salons = get_salons('chicago_salons.json')
    
  