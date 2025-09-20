from django.shortcuts import render,get_object_or_404
from app.models import *

# Create your views here.
def home(request):
    return render(request,'main.html',{'AUM_by_fund_types': AUM_by_fund_types()})  

def AUM_by_regNo(request, regNo):
    fund = get_object_or_404(Fund, regNo = regNo)
    return render(request,'regNo.html',{'total_AUM': fund.netAsset})

def AUM_by_fund_types():
    funds = Fund.objects.all()
    fundTypes = set()
    for fund in funds:
        fundTypes.add(fund.fundType)
    AUM_by_fund_types = {}
    for fundType in fundTypes:
        AUM = sum(fund.netAsset for fund in funds if fund.fundType == fundType and fund.netAsset)
        AUM_by_fund_types[fundType] = AUM
    return AUM_by_fund_types