from django.shortcuts import render ,redirect
def index(request):
    par1 = "Often , people need a specific medication. But sometimes they may not find it in the pharmacy , or they may not have enough money to buy it. With MedicaShare you can request the medication and resolve your problem in a short time"
    par2 = "Lots of people have medication that they don't use it .With MedicaShare you can donate this medications to the people who needs it and solve thier problem.<br/>   I cannot do all the good that the world needs. But the world needs all the good that I can do"
    if request.user.is_authenticated :
        return redirect(f'/')
    return render(request,'index.html',{'par1':par1,'par2':par2})
