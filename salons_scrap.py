import time
import requests
import pandas as pd
import json
import os

HEADERS = {
    "Cookie": '''QuantumMetricUserID=b193de7a702ea31c7992591895da2363; s_fid=67D81E4F99537405-10EC592C26A802C0; rxVisitor=17392591203047QN7Q7GD10M5U99PSIS4LUOIK3H2KDR5; _gcl_au=1.1.979278188.1739259125; s_ecid=MCMID%7C28614217048021289851963175683140868194; __tvpa=22c931a3f078d38e8a78d88dce8d0639; _scid=ghmZikNZuMQXESLDjAjB7HkuVQZDdei9; _caid=57b153d1-f493-4494-9906-94a63261c146; _fbp=fb.1.1739259312021.312852665719427203; _tt_enable_cookie=1; _ttp=6GlUnTLDc2SN3RNkVadDY3T6FL-.tt.1; _ScCbts=%5B%5D; _pin_unauth=dWlkPU0yUXpaRGMyTXpBdFlUaGpPUzAwWkdJMExXSmxOR1F0WmpSak1tRXhORGRtWm1Saw; _sctr=1%7C1739214000000; s_vi=[CS]v1|33D63E69DE64510C-4000077C41D2A802[CE]; _gid=GA1.2.206218391.1739561092; AKA_A2=A; dtPC=17$212310105_888h1vCKUBVJRIMNBFALHOVKPHCHAGESJPEFNN-0e0; dtSa=-; rxvt=1739614117936|1739612310111; AMCVS_C218F16F55CC57607F000101%40AdobeOrg=1; s_cc=true; QuantumMetricSessionID=ac59e0c5d80adc6f8d3fc8802c97f41b; IR_gbd=ulta.com; utag_ck_gtid=undefined; dtCookie=v_4_srv_19_sn_4FA51C1691E580ED9AD2088839BEC9F9_perc_100000_ol_0_mul_1_app-3Aaef46558697bc6fc_0_app-3A6fe4664190660d01_0_app-3Aea7c4b59f27d43eb_1_rcs-3Acss_0; IR_3037=1739613334207%7C0%7C1739613334207%7C%7C; gpv=beauty%20services%3Aall; __gads=ID=96677f85cc2f11db:T=1739259121:RT=1739613333:S=ALNI_MYav-yJv0kXy3r-UmF7UlVabmjO1g; __gpi=UID=00000fe36f9c3074:T=1739259121:RT=1739613333:S=ALNI_MZFaazIQVH7TGFUnQt8_kolRes6QQ; __eoi=ID=223dd917e7b52aa2:T=1739259121:RT=1739613333:S=AA-AfjYxczT-k6EcJyOSgvSwYbH3; _cavisit=1950908ee1d|; _rdt_uuid=1739259309694.1365b986-07de-46a1-8c1d-744a89613aa1; _rdt_em=3c010e52ef16c7ba1833f047620363a56abe3a830278bab612fba18782f6e6cb; _scid_r=kpmZikNZuMQXESLDjAjB7HkuVQZDdei9R_DeIg; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.ulta.com%252Fbeautyservices%252Fall; _derived_epik=dj0yJnU9X1ZTVk9Vc21BNzZ5ZmIzRnZmWE5IQlNFWGRnT2U0ZlUmbj10N3BFUWpTdXZGUmJkVXFfZzBOcDN3Jm09MSZ0PUFBQUFBR2V3WkpnJnJtPTEmcnQ9QUFBQUFHZXdaSmcmc3A9NQ; ABTasty=uid=2g3f0r93b2rd253j&fst=1739259126748&pst=1739561545674&cst=1739613336112&ns=3&pvt=14&pvis=1&th=1051085.1305480.2.2.1.1.1739259436144.1739259602027.1.1_1314523.1629097.14.1.3.1.1739259126813.1739613336220.0.3; s_nr=1739613337784-Repeat; AMCV_C218F16F55CC57607F000101%40AdobeOrg=1176715910%7CMCIDTS%7C20134%7CMCMID%7C28614217048021289851963175683140868194%7CMCAAMLH-1740218138%7C3%7CMCAAMB-1740218138%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739620538s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.4.0; RT="z=1&dm=ulta.com&si=23dc39c6-96a9-4234-a81a-5b05f767879a&ss=m76091di&sl=2&tt=j9h&rl=1&nu=1lpqgm1x&cl=m4pg&obo=1&ld=mbvt&r=210klr6h&hd=mbvu"; _ga=GA1.1.1825889827.1739259126; jwt=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ODRiMGVhLWUyMWMtNGQyMi04MGFmLTQ1MWRiM2QzYmNkZCIsInBob25lTnVtYmVyIjoiKzEgOTE5LTM3NC0wMjExIiwiZmlyc3ROYW1lIjoiTXVoYW1tYWQiLCJsYXN0TmFtZSI6IlJhemEiLCJpYXQiOjE3Mzk2MTM1NDQuMTUyLCJleHAiOjE3Mzk2MTUzNDQsImp0aSI6ImRiZWQ0YWIyLWQzYzYtNDE4Zi1hNDFhLTY1YTg2ZjdkZjJhMyJ9.lXgarxXPUhQ_vXVY-ItakNTaUiNkYH4Nva0CO2XAQIXSeAYEtmE4SYVo2qeyMSMqHvd1L8tjzTvS5hG4W7B1dg; refreshToken=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ODRiMGVhLWUyMWMtNGQyMi04MGFmLTQ1MWRiM2QzYmNkZCIsInBob25lTnVtYmVyIjoiKzEgOTE5LTM3NC0wMjExIiwiZmlyc3ROYW1lIjoiTXVoYW1tYWQiLCJsYXN0TmFtZSI6IlJhemEiLCJpYXQiOjE3Mzk2MTM1NDQuMTUyLCJleHAiOjE3NDQ3OTc1NDQsImp0aSI6IjRlZDlhYzU0LTg4YzAtNDMyYS1hNDZhLWZlZjA2MzQwNDM4NiJ9.WVJ0Vi4uNyjcdAYGXFqWEoN2jRvo0iS1M5G40ntiFM_VmeMPLER-J4KpF8tQ_rXT3RZbOthaPlop2EL658rNYA; BELLA_REMEMBER_ME=true; _ga_LKM7RC8LP8=GS1.1.1739612322.11.1.1739613930.60.0.0; utag_main=v_id:0194f3eb124300201459cdf014ac0506f002506700918$_sn:8$_se:29$_ss:0$_st:1739615732142$vapi_domain:ulta.com$ses_id:1739612313778%3Bexp-session$_pn:7%3Bexp-session; s_sq=%5B%5BB%5D%5D'''
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
            people_count=0
            # each dict have a specializiation field if that contains stylist text then we can count that stylist
            for stylist in stylist_data:
                if 'firstName' in stylist:
                    people_count+=1
                if 'specialization' in stylist and "Stylist" in stylist['specialization']:
                    stylist_count+=1
                if 'categories' in stylist:
                    for category in stylist['categories']:
                        if category.get('name') == 'Curls, Coils & Waves':
                            stylist_having_curls+=1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stylist data for location {locationID}: {e}")
            break
        
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
            "No of Professionals": people_count,
            'No of Stylists': stylist_count,
            'No of Stylist offering Curls, Coils & Waves': stylist_having_curls
        }
        
        print(location_data)
        appendProduct('ulta-salons.csv', location_data)
        time.sleep(1)

if __name__ == '__main__':
    salons = get_salons('chicago_salons.json')
    
  