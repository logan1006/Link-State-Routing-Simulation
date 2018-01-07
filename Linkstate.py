import csv
import sys
import os
import os.path
import heapq




print("\n*****************************************Hello Professor Choi Please select Option*********************************************************************************************")
print(" < CS542 Link State simulator  >")
print("**************************************************************************************************************************************\n")
print("Please choose option from the list :\n")
print("(1) Create a Network Topology")
print("(2) Build a Forward Table")
print("(3) Shortest Path to Destination Router")
print("(4) Modify a Topology (Change the status of the Router) ")
print("(5) Best Router for Broadcast ")
print("(6) Exit\n")
print("**************************************************************CS542 Link State simulator********************************************************************")
print("*******************************************************************Computer Networks 1 My best Course*******************************************************************\n")


class switch(object):
    command = None

    def __new__(prompt, command):
        prompt.command = command
        return True

def case(*choice):
    return any((option == switch.command for option in choice))

def dijkstra(origin):    # dijkstra logic 

    global distance_d
    global closed
    global last_n
    global open_n
    global link_connection
    closed = {}
    open_n = {}
    last_n = {}
    index_n = origin
    node_dist = 0
    link_connection = {}
    for v in nodes_n:
        link_connection[v] = []
        closed[v] = float('inf')
    closed[index_n] = node_dist
    while len(closed) > 0:
        for new_vertex, cost in distance_d[index_n].items():
            if new_vertex not in closed:
                continue
            new_cost = node_dist + cost
            if new_cost < closed.get(new_vertex, float('inf')):
                closed[new_vertex] = new_cost
                last_n[new_vertex] = index_n
                if not link_connection[index_n]:
                    link_connection[new_vertex] = [new_vertex]
                else:
                    link_connection[new_vertex] = list(link_connection[index_n])
        open_n[index_n] = node_dist
        del closed[index_n]
        if not closed:
            break
        new_state = []
        for v in closed.items():
            if v[1]:
                new_state.append(v)
        index_n, node_dist = sorted(new_state, key=lambda x: x[1])[0]

def error_check():  # check if invalid option is scanned 

    while True:
        try:
            n = int(input("Please Enter Command: \n"))
            return n
        except ValueError:
            print("Wrong input not an integer!  enter between option 1 to 6")
            continue
        else:
            break

def matrx(num_of_nodes,xoxo):   #matrix printer 

    if xoxo == 0:
        for i in range(num_of_nodes):
            net_mat = {j+1 : net_graph[i][j] for j in range(num_of_nodes) if i != j and net_graph[i][j] != -1}
            distance_d[i + 1] = net_mat
            nodes_n.append(i + 1)
        return distance_d, nodes_n
    else:
        for i in range(num_of_nodes):
            net_mat = {j+1 : net_graph[i][j] for j in range(num_of_nodes) if i != j != z and i != j and net_graph[i][j] != -1}
            distance_d[i + 1] = net_mat
        return distance_d, 0

def file_read(file):  #reading the file 

    global distance_d
    global net_graph
    global nodes_n
    global num_of_nodes
    if (not file.endswith('.txt')):
        print("Invalid file format")
        pass
    elif not os.path.isfile(file):
        print("File not Found")
        pass
    elif os.stat(file).st_size == 0:
        print("File is empty")
        pass
    else:
        print("\nReview Original Topology net_mat")
        with open(file) as net_topo:
            net_graph = []
            for x in net_topo:
                net_graph.append(list(map(int, x.split())))
        for line in net_graph:
            for item in line:
                print(item, end='    ')
            print()
        num_of_nodes = len(net_graph)
        print("\nTotal number of nodes present: ", num_of_nodes)
        xoxo = 0
        distance_d, nodes_n = matrx(num_of_nodes,xoxo)
        print("\nFinal net_graph dictionary - ", distance_d)
        return distance_d

def conn_table():  # creating connection table 

    for key in link_connection:
        print("\t",key, "\t\t", link_connection[key])

def seen(f,lst):

    dijkstra(f)
    l = 0
    for k, v in open_n.items():
        l = l + v
    print("\t",f,"\t\t", l)
    lst.append(l)
    return lst

def best_rout(tt,query):  # best broadcast router 

    fin_l = []
    fin = []
    if query == 1:
        for i in range(1,tt+1):
            lst = seen(i,fin_l)
        u = min(fin_l)
        v = lst.index(u)
        return u,v
    elif query == 2:
        for i in tt:
            fin_l = seen(i,fin_l)
            fin.append(i)
        u = min(fin_l)
        v = fin_l.index(u)
        t = fin[v]
        return u,t

def main():

    n = error_check()
    if n != 1:
        print("Import input File by Choosing option 1")
        n = error_check()
    
    while switch(n):

        if case(1):
            print("\nInput original network topology net_mat data file in (.txt) format:\n")
            file = input()
            distance_d = file_read(file)

            n = error_check()
            switch(n)

        if case(2):
            print("\nSelect a source router:")
            origin = error_check()
            if  origin < 1 or origin > len(distance_d) :
                print("Enter valid router")
                continue
            dijkstra(origin)
            print("\nRouter %s Connection Table:"%origin)
            print("target\tInterface")
            conn_table()
            n = error_check()
            switch(n)

        if case(3):
            print("\nSelect the target router:")
            target = error_check()

            if  target < 1 or target > len(distance_d) :
                print("Enter valid router")
                continue
            elif target == origin:
                print("Source and Destinaton Routers are Same")
                continue
            new_desti = target
            print("\nMinimum Cost from %s to %s is %s" % (origin, target, open_n[target]))
            path = []
            while 1:
                path.append(target)
                if target == origin:
                    break
                target = last_n[target]
            path.reverse()
            target = new_desti
            print("\nShortest Path from %s to %s is %s"%(origin,target,path))
            print("Enter Command:\n 4 for modification: \n 5 for Best Router: \n")
            n = error_check()
            switch(n)

        if case(4):
            global closed
            global z
            #global target
            print("\nSelect a Router to be Removed:")
            down_router = error_check()

            if down_router < 1 or down_router > len(distance_d):
                print("Enter valid Router")
                continue
            z = down_router - 1
            xoxo = 1
            distance_d, xo = matrx(num_of_nodes, xoxo)
            del distance_d[down_router]
            del nodes_n[z]
            if down_router == origin:
                origin = int(input("Enter new origin node\n"))
            dijkstra(origin)

            print("\nRouter %s Connection Table:" % origin)
            print("target\tInterface")
            conn_table()
            path = []
            nxt_desti = target
            print(nxt_desti)
            if down_router == target:
                target = int(input("Please enter new target router"))
                nxt_desti = target
            while 1:
                path.append(target)
                if target == origin:
                    break
                target = last_n[target]
            path.reverse()
            target = nxt_desti
            print("Updated Shortest Path is:",path)
            print("Updated shortest distance",open_n[target])
            h = [k for k,v in distance_d.items()]
            n = error_check()
            switch(n)

        if case(5):

            lst = []
            lt = []
            print("\nSelect one of the options:\n")

            print("1 - Topology map not Updated: Best Broadcast Router for original graph")
            print("2 - Topology map is  updated: Best Router Broadcast for updated graph")

            query = error_check()

            #if query < 1 or query > 2:
                #print("Please choose either option 1 or option 2")
                #continue
            print("nodes_n\tTotal_Cost")
            if int(query) == 1:
                u,v = best_rout(num_of_nodes,query)
                print("\nBest Router is %s with lowest cost %s" % (v + 1, u))
            elif int(query) == 2:
                u,t = best_rout(h,query)
                print("\nBest Router is %s with lowest cost %s"%(t,u))
                print("\nExit CS542-04 2017 Fall project.  Good Bye! ")
                break
   
        if case(6):
            print("\nExit CS542-04 2017 Fall project.  Good Bye! ")
            break
        

if __name__ == '__main__':
    global target
    net_graph = []
    distance_d = {}
    nodes_n = []
    link_connection = {}
    path = []
    main()