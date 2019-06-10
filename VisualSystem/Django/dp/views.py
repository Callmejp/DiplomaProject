from django.shortcuts import render
from django.http import JsonResponse
import os
import pickle


def analyzeHandle(file, filename):
    rstList = []
    file_path = os.path.join('upload', filename)

    f = open(file_path, 'wb')
    for i in file.chunks():
        f.write(i)
    f.close()
 
    try:
        with open('/home/ubuntu/mystite/upload/'+filename, 'rb') as fileHandle:
            rstList = pickle.load(fileHandle)
    except FileNotFoundError:
        print(filaname + "not found!")

    for ele in rstList[::-1]:
        if ele < 0:
            rstList.remove(ele)
            continue
    
    return rstList


def analyzeResult(request): 
    result = {"result_1": [], "result_2": []}

    result_one = request.FILES.get('rst')
    result_two = request.FILES.get('rst1')

    result["result_1"] = analyzeHandle(result_one, 'result1.txt')
    result["result_2"] = analyzeHandle(result_two, 'result2.txt')

    return JsonResponse(result, safe=False)    


def queryResult(request):
    result = {"end_1": False, "end_2": False, "list_1": [], "list_2": []}
    testList, testList_2 = [], []
    
    try:
        with open('/home/ubuntu/mystite/upload/1.txt', 'rb') as fileHandle:
            testList = pickle.load(fileHandle)
    except FileNotFoundError:
        print("1.txt not found")
   
     
    result["list_1"] = testList

   
    if len(testList) >= 100:
        result["end_1"] = True
        try:
            with open('/home/ubuntu/mystite/upload/2.txt', 'rb') as fileHandle_2:
                testList_2 = pickle.load(fileHandle_2)
        except FileNotFoundError:
            print("2.txt not found")

        result["list_2"] = testList_2

    if len(testList_2) >= 100: 
        result["end_2"] = True
    
    """
    if result["end_1"] and result["end_2"]:
        os.remove('/home/ubuntu/mystite/upload/1.txt')
        os.remove('/home/ubuntu/mystite/upload/2.txt')
    """
    return JsonResponse(result, safe=False)


def twoCharts(request):
    flag = request.POST.get('flag')

    testList, testList_2 = [], []
    result = {"rst1": [], "rst2": []}    
    
    if flag == 0:
        with open('/home/ubuntu/mystite/upload/1.txt', 'rb') as fileHandle:
            testList = pickle.load(fileHandle)
   
        with open('/home/ubuntu/mystite/upload/2.txt', 'rb') as fileHandle_2:
            testList_2 = pickle.load(fileHandle_2)
        
        os.remove('/home/ubuntu/mystite/upload/1.txt')
        os.remove('/home/ubuntu/mystite/upload/2.txt')
    else:
        with open('/home/ubuntu/mystite/upload/result1.txt', 'rb') as fileHandle:
            testList = pickle.load(fileHandle)
   
        with open('/home/ubuntu/mystite/upload/result2.txt', 'rb') as fileHandle_2:
            testList_2 = pickle.load(fileHandle_2)
        
    for i in range(100):
        if testList[i] >= 0 and testList_2[i] >= 0:
            result["rst1"].append(testList[i])
            result["rst2"].append(testList_2[i])
 
    return JsonResponse(result, safe=False)



def testHandle(network, filename):
 
    net_format = str(network.name).split('.')[1]
    
    file_path = os.path.join('upload', filename + net_format)

    f = open(file_path, 'wb')
    for i in network.chunks():
        f.write(i)
    f.close()

    return '../../mystite/' + str(file_path)


import threading
import time


def test(request):
    result = {"wait": 0}
    if os.path.exists('/home/ubuntu/mystite/upload/1.txt'):
        result['wait'] = 1
        return JsonResponse(result, safe=False)
    network_one = request.FILES.get('file')
    network_two = request.FILES.get('file1')
   
    fp1 = testHandle(network_one, '1.')
    fp2 = testHandle(network_two, '2.')
    """
    test = PrintThread(args=(file_path_one, file_path_two,))
    test.start()
    """
    tempThread = threading.Thread(target=CallSh, args=(fp1, fp2, ))
    tempThread.start()    

    return JsonResponse(result, safe=False)


"""
class PrintThread(threading.Thread):
    def run(self):
        
        print("start.... %s" % (self.getName(),))
        network_path_1 = '../../networks/convSmallRELU__Point.pyt'
        os.system('sh test.sh '+network_path_1)
        print("end.... %s"%(self.getName(),))
        
        print(p1, p2)
        cmd = 'sh test.sh ' + file_path_one + ' ' + file_path_two
        print(cmd)
        os.system(cmd)
"""
def CallSh(p1, p2): 
    cmd = 'sh test.sh ' + p1 + ' ' + p2
    os.system(cmd)

