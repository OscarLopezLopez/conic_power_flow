# Importing required libraries
import numpy as np
import cmath


class grid:
    def __init__(self, nodes, lines, pros):
        self.nodes = self.add_nodes(nodes)                                      
        self.lines = self.add_lines(lines, self.nodes)  
        self.pros = self.add_pros(pros, self.nodes)  
                
    def add_nodes(self, nodes):
        nodes_list = list()
        for item in nodes:
            nodes_list.append(node(item['id'], item['slack']))
        return nodes_list
        
    def add_lines(self, lines, nodes):
        lines_list = list()
        for item in lines:
            lines_list.append(line(item['id'], item['From'], item['To'], item['R'], item['X'], nodes))
        return lines_list
        
    def add_pros(self, pros, nodes):
        pros_list = list()
        for item in pros:
            pros_list.append(prosumer(item['id'], item['Node'], item['P'], item['Q'], nodes))
        return pros_list
    
    def pf(self):
        n = len(self.nodes)
        m = len(self.lines)
        x_size = n+(2*m)
        # columna_inicial = 1   #Para bucle con while

        matrizA = np.zeros((2*n, n+2*m), dtype=float)
        matrizB = np.zeros((2*n,1), dtype=float)
        matrizX = np.zeros((x_size,1), dtype=float)
        matrizX1 = np.zeros((n, 1), dtype=float)
        matrizX2 = np.zeros((m, 1), dtype=float)           
        matrizX3 = np.zeros((m, 1), dtype=float)
                            
        #MATRIZ B
        for i, node in enumerate(self.nodes):
            for x in node.pros:
                matrizB[2*i] = x.P
                matrizB[(2*i)+1] = x.Q
        
        
        #MATRIZ X
        #Listas Ckk, Ckt y Skt que formen la matriz X total
        n_aux = 0
        # while n_aux < n:
        #     matrizX1[n_aux] = self.nodes[n_aux].Ckk
        #     n_aux += 1
        
        # n_aux = 0    
        # while n_aux < m:
        #     matrizX2[n_aux] = self.lines[n_aux].Ckt
        #     n_aux += 1
        
        # n_aux = 0
        # while n_aux < m:
        #     matrizX3[n_aux] = self.lines[n_aux].Skt
        #     n_aux += 1
        
        while n_aux < n:
            self.nodes[n_aux].Ckk = n_aux
            n_aux += 1
        
        n_aux2 = 0    
        while n_aux2 < m:   
            self.lines[n_aux2].Ckt = n_aux
            n_aux += 1
            n_aux2 += 1
        
        n_aux3 = 0    
        while n_aux3 < m:   
            self.lines[n_aux3].Skt = n_aux
            n_aux += 1
            n_aux3 += 1        
       
        matrizX1 = np.array([node.Ckk for node in self.nodes]).reshape(n, 1)
        matrizX2 = np.array([line.Ckt for line in self.lines]).reshape(m, 1)           
        matrizX3 = np.array([line.Skt for line in self.lines]).reshape(m, 1)     
        matrizX = np.vstack((matrizX1, matrizX2, matrizX3))  #Concatena las 3 arrays en vertical.

        print("Los índices de la matriz X relacionados con la línea 0 son: \n", self.lines[0].Ckt,",", self.lines[0].Skt)        

    
        #MATRIZ A
        #El nudo 0 es slack, por lo que las 2 primeras filas son 0.
        for i in range(2, 2*n, 2):
            lineas = []
            for linea in self.lines:
                if linea.nodes[0].ref == i/2 or linea.nodes[1].ref == i/2:
                    lineas.append(linea)
            
            print("Las líneas pertenecientes al nodo", int(i/2) , "son:")
            print(lineas)
            print("")
            
            # j = columna_inicial
            # while j < x_size:
            #     SumaG, SumaB = self.cuenta_1(columna_inicial, lineas)
            #     G_ant, B_ant = self.cuenta_2(columna_inicial, lineas)
            #     G_post, B_post = self.cuenta_3(columna_inicial, lineas)
            #     print(f"Valor de la G de la línea que entra en el nodo: ", lineas[0].G)
            #     print("")
                
            #     if (columna_inicial) < matrizA.shape[1]:
            #         matrizA[i, columna_inicial] = SumaG  #Para la fila de P
            #         matrizA[(i+1), columna_inicial] = SumaB  #Para la fila de Q
               
            #     if (columna_inicial + 3) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+3)] = -G_ant
            #         matrizA[(i+1), (columna_inicial+3)] = -B_ant
                
            #     if (columna_inicial + 4) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+4)] = -G_post
            #         matrizA[(i+1), (columna_inicial+4)] = -B_post
                
            #     if (columna_inicial + 6) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+6)] = -B_ant
            #         matrizA[(i+1), (columna_inicial+6)] = G_ant
                
            #     if (columna_inicial + 7) < matrizA.shape[1]:
            #         matrizA[i, (columna_inicial+7)] = -B_post
            #         matrizA[(i+1), (columna_inicial+7)] = G_post
                
            #     j += 1
                
            # columna_inicial += 1
            
            for j in range(i // 2, x_size):
                columna = j
                SumaG, SumaB = self.cuenta_1(lineas)
                G_ant, B_ant = self.cuenta_2(lineas)
                G_post, B_post = self.cuenta_3(lineas)
                
                if (columna) < matrizA.shape[1]:
                    matrizA[i, columna] = SumaG  #Para la fila de P
                    matrizA[(i+1), columna] = SumaB  #Para la fila de Q
               
                if (columna + 3) < matrizA.shape[1]:
                    matrizA[i, (columna+3)] = -G_ant
                    matrizA[(i+1), (columna+3)] = -B_ant
                
                if (columna + 4) < matrizA.shape[1]:
                    matrizA[i, (columna+4)] = -G_post
                    matrizA[(i+1), (columna+4)] = -B_post
                
                if (columna + 6) < matrizA.shape[1]:
                    matrizA[i, (columna+6)] = -B_ant
                    matrizA[(i+1), (columna+6)] = G_ant
                
                if (columna + 7) < matrizA.shape[1]:
                    matrizA[i, (columna+7)] = -B_post
                    matrizA[(i+1), (columna+7)] = G_post
                
                # print(f"Valor de la posición ({i}.{columna}) de la matriz A: ", matrizA[i, columna])
                # print("")                   
                break         
            
        print("La matriz B es:\n")
        print(matrizB)
        print("")
        print("La matriz X es:\n")
        print(matrizX)
        print("")
        print("La matriz A es:\n")
        print(matrizA)
        print("")
        print("Al final, el resultado de A*x = b es: \n")
        print(f"{matrizA} * {matrizX} = {matrizB}")
    def cuenta_1 (self, lineas):
        Suma1 = sum(linea.G  for linea in lineas)
        Suma2 = sum(linea.G  for linea in lineas)
        return Suma1, Suma2
    def cuenta_2 (self, lineas):
        G_anterior = lineas[0].G
        B_anterior = lineas[0].B
        return G_anterior, B_anterior
    def cuenta_3 (self, lineas):
        if len(lineas) > 1:
            G_posterior = lineas[1].G
            B_posterior = lineas[1].B
        else:
            G_posterior = 0
            B_posterior = 0
        return G_posterior, B_posterior


class node:
    def __init__(self, ref, slack):
        self.ref = ref   
        self.slack = slack        
        self.lines = list()
        self.pros = []
        self.Ckk = []
        
class line:
    def __init__(self, ref, From, To, R, X, nodes_list):
        self.ref = ref     
        self.Z = complex(R, X)
        self.G, self.B = np.real(1/self.Z), -np.imag(1/self.Z)
        self.Y = 1/self.Z
        self.nodes = [next((item for item in nodes_list if item.ref == From), None), 
                      next((item for item in nodes_list if item.ref == To), None)]   
        self.nodes[0].lines.append(self)
        self.nodes[1].lines.append(self)
        self.Ckt = []
        self.Skt = []
    
class prosumer:
    def __init__(self, ref, node_id, P, Q, nodes_list):
        self.ref = ref
        self.P = P
        self.Q = Q        
        self.node = next((item for item in nodes_list if item.ref == node_id), None)
        self.node.pros.append(self)
        
        
        
        
        
       
        
        
        
        
    