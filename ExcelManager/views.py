from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .models import Classes, BalanceAccounts, Files, Records
import os
import xlrd
from datetime import datetime
from dateutil import parser



def parseAndSaveFile(f):
    f = str(f)
    rd = xlrd.open_workbook(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\Files\\test.xls')
    if rd is None:
        print("ERROR")
        return
    sheet = rd.sheet_by_index(0)
    rownum = sheet.nrows
    file = Files()
    classes = None

    for numberOfRow in range(rownum):
        row = sheet.row_values(numberOfRow)
        if type(row[0]) is str:
            if row[0].__contains__('КЛАСС '):
                class_number = int(row[0].split('  ')[1])
                descr = row[0].split('  ')[2]
                if len(Classes.objects.filter(ClassNumber=class_number)) == 0:
                    classes = Classes(ClassNumber=class_number, Description=descr)
                    classes.save()
                classes = Classes.objects.get(ClassNumber=class_number)
                classes.ClassNumber = class_number
                classes.Description = descr
                print("class's class_number : ", row[0].split('  ')[1])
                print("class's descr : ", row[0].split('  ')[2])
                continue
            else:
                if classes is not None:
                    bAccount = None
                    if len(row[0]) > 4 or len(row[0]) < 3:
                        continue
                    if len(BalanceAccounts.objects.filter(Number=int(row[0]))) == 0:
                        bAccount = BalanceAccounts(ClassId=classes, Number=int(row[0]))
                        bAccount.save()
                    bAccount = BalanceAccounts.objects.get(Number=int(row[0]))
                    record = Records()
                    record.FileId = file
                    record.BalanceAccountsId = bAccount
                    record.IncomingBalanceAssets = row[1]
                    record.OutgoingBalanceAssets = row[5]
                    record.IncomingBalanceLiabilities = row[2]
                    record.OutgoingBalanceLiabilities = row[6]
                    record.CirculationDebit = row[3]
                    record.CirculationCredit = row[4]
                    record.save()


def index(request):
    return render(request, 'ExcelManager/upload.html')

class IndexView(generic.ListView):
    template_name = 'ExcelManager/index.html'
    context_object_name = 'all_files'

    def get_queryset(self):
        return Files.objects.filter()


def details(request, Id):
    file = Files.objects.get(Id=Id)
    bAccaunts = BalanceAccounts.objects.all()
    records = []
    row_number = 1
    for acc in bAccaunts:
        l = Records.objects.get(FileId=Id, BalanceAccountsId=acc.Id).getList()
        l.insert(0, acc.Number)
        l.insert(0, row_number)
        row_number += 1
        records.append(l)

    resultsL = Records.objects.filter(FileId=Id)
    result = Records().getZerous()
    for res in resultsL:
        result + res
    results = result.getList()
    return render(request, 'ExcelManager/success.html',
                  {'file': file,
                   'records': records,
                   'results': results})



def handle_uploading_file(f):
    with open('D:\\work\\excel_task\\Files\\test.xls', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if len(Files.objects.filter(Name=str(f))) != 0:
        return 1
    else:
        parseAndSaveFile(f)
        return 0


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            res = handle_uploading_file(request.FILES['file'])
            if res == 0:
                return HttpResponseRedirect('/success/')
            else:
                form = UploadFileForm()
                return render(request, 'ExcelManager/upload.html',
                              {'form': form, 'message': 'such file has already been uploaded'})
    else:
        form = UploadFileForm()
    return render(request, 'ExcelManager/upload.html', {'form': form, 'message': ''})
