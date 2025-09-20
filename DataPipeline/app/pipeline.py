import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DataPipeline.settings")
django.setup()


import requests
from pydantic import ValidationError
from app.pydantic_models import *
from app.models import *
from prefect import flow,task


@task
def get_API_data(url):
    response = requests.get(url)
    return response.json()

@task
def validate_data(data):
    try:
        api_response = FundAPIResponse(**data)
    except ValidationError as e:
        print("Validation Error")
        print(e.json())
    return api_response.items

@task
def update_funds_list(api_funds):
    insert_funds = []
    update_funds = []
    for api_fund in api_funds:
        try:
            filtered_fund = Fund.objects.get(regNo=api_fund.regNo)
            if(filtered_fund.name!=api_fund.name or filtered_fund.fundType!=api_fund.fundType
                    or filtered_fund.netAsset!=api_fund.netAsset):
                    update_funds.append((filtered_fund,{'name': api_fund.name,'fundType':api_fund.fundType,
                                                        'netAsset':api_fund.netAsset}))   
        except:
                new_fund = Fund(regNo = api_fund.regNo,name = api_fund.name,
                                     fundType = api_fund.fundType, netAsset = api_fund.netAsset)
                insert_funds.append(new_fund)
        
    return insert_funds,update_funds

@task   
def insert_into_db(insert_funds):
    Fund.objects.bulk_create(insert_funds)
    print(insert_funds)
    print(len(insert_funds),' items inserted!')

@task
def update_db_funds(update_funds):
    for update_fund in update_funds:
        fund = update_fund[0]
        values = update_fund[1]
        fund.name = values['name']
        fund.fundType = values['fundType']
        fund.netAsset = values['netAsset']
        fund.save()
    
    print(update_funds)
    print(len(update_funds),' items updated!')
            

@flow
def run():
    url = "https://fund.fipiran.ir/api/v1/fund/fundcompare"
    data = get_API_data(url)
    api_funds = validate_data(data)
    insert_funds,update_funds = update_funds_list(api_funds)
    insert_into_db(insert_funds)
    update_db_funds(update_funds)

if __name__ == "__main__":
    run()