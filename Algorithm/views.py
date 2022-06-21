from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import re
from queue import PriorityQueue
#Check if the string starts with "The" and ends with "Spain":

"""_summary_
    {'Arad': {'Zerind': '', 'Timisoara': '', 'Sibiu': ''}, 'Zerind': {'Oradea': '', 'Arad': ''}, 'Oradea': {'Sibiu': ''}, 'Sibiu': {'Rimniciu Vilcea': '', 'Fagaras': '', 'Arad': ''}, 'Fagaras': {'Sibiu': '', 'Bucharest': ''}, 'Rimniciu Vilcea': {'Pitesti': '', 'Craiova': '', 'Sibiu': ''}, 'Timisoara': {'Lugoj': '', 'Arad': ''}, 'Lugoj': {'Mehadia': ''}, 'Mehadia': {'Lugoj': '', 'Dorbeta': ''}, 'Dorbeta': {'Mehadia': '', 'Craiova': ''}, 'Pitesti': {'Craiova': '', 'Bucharest': ''}}
    """
#if(re.search("^City[0-9]$", x)):
      #      cc[x]=request.POST[x]
       # if(re.search("^heuristicCity[0-9]$", x)):
        #    hh[x]=request.POST[x]
        #if(re.search("^City[0-9]toCity[0-9]$", x)):
        #    dd[x]=request.POST[x]
        #if(re.search("^City1toCity[0-9]cost$", x)):
        #    cost1[x]=request.POST[x]
        #if(re.search("^City2toCity[0-9]cost$", x)):
        #    cost2[x]=request.POST[x]
        #if(re.search("^City3toCity[0-9]cost$", x)):
        #    cost3[x]=request.POST[x]
    #print(cc)
    #print(hh)
    #print(dd)
    #print(cost1)
"""
    for x in cost1:
        boss1[dd[x[:(len(x)-4)]]]=cost1[x]
    print(boss1)
    for x in cost2:
        boss2[dd[x[:(len(x)-4)]]]=cost2[x]
    print(boss2)
    for x in cost3:
        boss3[dd[x[:(len(x)-4)]]]=cost3[x]
    print(boss3)
    if(len(cc.keys()) and len(boss1.keys()) and len(boss2.keys()) and len(boss3.keys())):
        boss={cc['City1']:boss1,cc['City2']:boss2,cc['City3']:boss3}
    print(boss)
    print(allO)
    for x in allO.keys():
        if(re.search("^City1toCity[0-9]cost$", x)):
            city1[allO['City1']][allO[x:(len(x)-4)]]=allO[x]
    print("city1",city1)"""
def index (request):
    allO={}
    Graph={}
    straight_line ={}
    for x in request.POST:
        if(re.search('[0-9]', x) and request.POST.get(x) !=""):
          allO[x]=request.POST[x]
     
    def create(city):
        mycity=city+"toCity[0-9]{1,}cost$"
        heuristic="heuristic"+city
        boss={}
        for x in allO.keys():
            if(re.search(heuristic, x)):
                straight_line[allO[city].strip()]=int(allO[x].strip())
            if(re.search(mycity, x)):
                boss[allO[x[:(len(x)-4)]].strip()]=int(allO[x].strip())
        if not Graph.get(allO[city]):
            Graph[allO[city].strip()]=boss
        return
    
    for x in allO.keys():
        if(re.search("^City[0-9]{1,}$", x.strip())):
            for q in Graph.keys():
                if q.strip()==allO[x].strip():
                    continue
            create(x)
    print(Graph)
    print(straight_line)
    
    def a_star(source, destination):
    
     p_q,visited = PriorityQueue(),{}
     p_q.put((straight_line[source], 0, source, [source]))
     visited[source] = straight_line[source]
     while not p_q.empty():
        (heuristic, cost, vertex, path) = p_q.get()
        print('Queue Status:',heuristic, cost, vertex, path)
        if vertex == destination:
           return heuristic, cost, path
        for next_node in Graph[vertex].keys():
            current_cost = cost + Graph[vertex][next_node]
            heuristic = current_cost + straight_line[next_node]
            if not next_node in visited or visited[next_node] >= heuristic:
                visited[next_node] = heuristic
                p_q.put((heuristic, current_cost, next_node,path + [next_node]))
    def main():
     try:
      print('Source :', end=' ')
      print('Destination :', end=' ')
      source=request.POST.get("sour")
      destination=request.POST.get("des")
      if source not in Graph or destination not in Graph:
        s="CITY DOES NOT EXIST."
        print(s)
        return ""
      else:
        heuristic, cost, optimal_path = a_star(source, destination)
        s="min of total heuristic_value ="+str(heuristic)+"\n"+"total min cost ="+str(cost)+"\nRoute:\n"+" -> ".join(city for city in optimal_path)
        print(s)
        """'min of total heuristic_value =', heuristic)
        print('total min cost =', cost)
        print('\nRoute:')
        print(' -> '.join(city for city in optimal_path))"""
        return s
     except Exception as e:
         return "Wrong!! please make sure you entre all cities with their info"
    main()
    return render(request,'index.html',{'result':main(),'GRAPH':Graph})