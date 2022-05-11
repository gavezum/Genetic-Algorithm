import tsplib95

#Include the name of the file that you want to test.
#Download the data in the website http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html and save as .tsp
Name_tsp_file = 'pr299.tsp'

problem = tsplib95.load(Name_tsp_file)
distance_matrix = []
for i in range(1,len(problem.node_coords)+1):
    aux=[]
    for j in range(1,len(problem.node_coords)+1):
        aux.append(problem.get_weight(i,j))
    distance_matrix.append(aux)