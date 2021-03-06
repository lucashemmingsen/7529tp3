import unittest
import types
from src.grafosimple import GrafoSimple
from src.flujo import Flujo

class TestGrafoSimple(unittest.TestCase):
    def test_vacio(self):
        grafo = GrafoSimple()
        Flujo.convertir(grafo)
        self.assertEqual(0,grafo.cantidadNodos())
        self.assertEqual(0,grafo.cantidadArcos())
        self.assertEqual(0,len(list(grafo.arcos())))

    def test_AB10_cantidad(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",10)

        Flujo.convertir(grafo)

        self.assertEqual(2,grafo.cantidadNodos())
        self.assertEqual(2,grafo.cantidadArcos())
        self.assertEqual(2,len(list(grafo.arcos())))

    def test_AB2AC3_cantidad_arcos(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("A","C",3)
        Flujo.convertir(grafo)
        desde0 = list(grafo.arcoDesdeNodoId(0))
        desde1 = list(grafo.arcoDesdeNodoId(1))
        desde2 = list(grafo.arcoDesdeNodoId(2))

        self.assertEqual(len(desde0), 2)
        self.assertEqual(len(desde1), 1)
        self.assertEqual(len(desde2), 1)
        self.assertEqual(4,grafo.cantidadArcos())
        self.assertEqual(3,grafo.cantidadNodos())

    def test_AB2AC3_arcos_orden(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("A","C",3)
        Flujo.convertir(grafo)
        AB, AC = list(grafo.arcoDesdeNodoId(0))
        BA = list(grafo.arcoDesdeNodoId(1))[0]
        CA = list(grafo.arcoDesdeNodoId(2))[0]
        self.assertEqual(  AB[0], 1 )
        self.assertEqual(  AC[0], 2 )
        self.assertEqual(  BA[0], 0 )
        self.assertEqual(  CA[0], 0 )

    def test_AB2AC3_arcos_inversos(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("A","C",3)
        Flujo.convertir(grafo)
        AB, AC = list(grafo.arcoDesdeNodoId(0))
        BA = list(grafo.arcoDesdeNodoId(1))[0]
        CA = list(grafo.arcoDesdeNodoId(2))[0]
        self.assertIs(AB[1].inverso(), BA[1])
        self.assertIs(AC[1].inverso(), CA[1])

    def test_AB2AC3CB1_bfs_existentes(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("A","C",3)
        grafo.insertarArcoConAlias("C","B",1)
        flujo = Flujo(grafo)
        self.assertEqual( flujo.bfs(0,1), [1] )
        self.assertEqual( flujo.bfs(0,2), [2] )
        self.assertEqual( flujo.bfs(2,1), [1] )

    def test_AB2AC3CB1_bfs_inexistentes(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("A","C",3)
        grafo.insertarArcoConAlias("C","B",1)
        flujo = Flujo(grafo)
        self.assertEqual( flujo.bfs(1,0), [] )
        self.assertEqual( flujo.bfs(1,2), [] )
        self.assertEqual( flujo.bfs(2,0), [] )

    def test_pentagono_bfs(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("B","C",2)
        grafo.insertarArcoConAlias("C","D",4)
        grafo.insertarArcoConAlias("D","E",3)
        grafo.insertarArcoConAlias("A","E",99)
        grafo.insertarArcoConAlias("A","D",50)
        flujo = Flujo(grafo)
        self.assertEqual( flujo.bfs(0,1), [1] )
        self.assertEqual( flujo.bfs(0,2), [1,2] )
        self.assertEqual( flujo.bfs(0,3), [3] )
        self.assertEqual( flujo.bfs(0,4), [4] )

    def test_pentagono_con_flujo_bfs(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",2)
        grafo.insertarArcoConAlias("B","C",2)
        grafo.insertarArcoConAlias("C","D",4)
        grafo.insertarArcoConAlias("D","E",3)
        grafo.insertarArcoConAlias("A","E",99)
        flujo = Flujo(grafo)
        flujo.fluir(2,3,2)
        flujo.fluir(3,4,1)
        self.assertEqual( flujo.bfs(0,1), [1] )
        self.assertEqual( flujo.bfs(0,2), [1,2] )
        self.assertEqual( flujo.bfs(0,3), [4,3] )
        self.assertEqual( flujo.bfs(0,4), [4] )

    def test_aumentar_camino_largo(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",11)
        grafo.insertarArcoConAlias("A","C",11)
        grafo.insertarArcoConAlias("C","D",11)
        grafo.insertarArcoConAlias("B","E",11)
        grafo.insertarArcoConAlias("D","E",11)
        grafo.insertarArcoConAlias("E","F",5)
        flujo = Flujo(grafo)
        flujo.aumentar(0,[2,3,4,5])
        arcos = [(u,v,w.valor()) for (u,v,w) in grafo.arcos()]
        arcos.sort()
        self.assertEqual(arcos, [
            (0,1,11), (0,2,6), (1,0,0), (1,4,11),
            (2,0, 5), (2,3,6), (3,2,5), (3,4, 6),
            (4,1, 0), (4,3,5), (4,5,0), (5,4, 5)
        ])

    def test_aumentar_camino_corto(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",11)
        grafo.insertarArcoConAlias("A","C",11)
        grafo.insertarArcoConAlias("C","D",11)
        grafo.insertarArcoConAlias("B","E",11)
        grafo.insertarArcoConAlias("D","E",11)
        grafo.insertarArcoConAlias("E","F",5)
        flujo = Flujo(grafo)
        flujo.aumentar(0,[1,4,5])
        arcos = [(u,v,w.valor()) for (u,v,w) in grafo.arcos()]
        arcos.sort()
        self.assertEqual(arcos, [
            (0,1,6), (0,2,11), (1,0,5), (1,4, 6),
            (2,0,0), (2,3,11), (3,2,0), (3,4,11),
            (4,1,5), (4,3,0), (4,5,0), (5,4, 5)
        ])

    def test_edmonds_2caminos(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("A","B",11)
        grafo.insertarArcoConAlias("A","C",11)
        grafo.insertarArcoConAlias("C","D",11)
        grafo.insertarArcoConAlias("B","E",11)
        grafo.insertarArcoConAlias("D","E",11)
        grafo.insertarArcoConAlias("E","F",5)
        flujo = Flujo(grafo)
        flujo.edmonds(0,5)
        arcos = [(u,v,w.valor()) for (u,v,w) in grafo.arcos()]
        arcos.sort()
        self.assertEqual(arcos, [
            (0,1,6), (0,2,11), (1,0,5), (1,4, 6),
            (2,0,0), (2,3,11), (3,2,0), (3,4,11),
            (4,1,5), (4,3,0), (4,5,0), (5,4, 5)
        ])

    def test_diapo3_flujo_maximo(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("a","b", 5)
        grafo.insertarArcoConAlias("c","b", 5)
        grafo.insertarArcoConAlias("a","d",10)
        grafo.insertarArcoConAlias("d","c", 2)
        grafo.insertarArcoConAlias("d","e",10)
        grafo.insertarArcoConAlias("c","f", 8)
        grafo.insertarArcoConAlias("f","g", 9)
        grafo.insertarArcoConAlias("s","a", 5)
        grafo.insertarArcoConAlias("s","c",20)
        grafo.insertarArcoConAlias("b","t", 5)
        grafo.insertarArcoConAlias("e","t",10)
        grafo.insertarArcoConAlias("g","t", 8)
        id_s = grafo.idDeNodoAlias("s")
        id_t = grafo.idDeNodoAlias("t")

        flujo = Flujo(grafo)
        fmax = flujo.edmonds(id_s,id_t)
        self.assertEqual(fmax,18)

    def test_diapo3_subconjunto_A(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("a","b", 5)
        grafo.insertarArcoConAlias("c","b", 5)
        grafo.insertarArcoConAlias("a","d",10)
        grafo.insertarArcoConAlias("d","c", 2)
        grafo.insertarArcoConAlias("d","e",10)
        grafo.insertarArcoConAlias("c","f", 8)
        grafo.insertarArcoConAlias("f","g", 9)
        grafo.insertarArcoConAlias("s","a", 5)
        grafo.insertarArcoConAlias("s","c",20)
        grafo.insertarArcoConAlias("b","t", 5)
        grafo.insertarArcoConAlias("e","t",10)
        grafo.insertarArcoConAlias("g","t", 8)
        id_s = grafo.idDeNodoAlias("s")
        id_t = grafo.idDeNodoAlias("t")

        flujo = Flujo(grafo)
        fmax = flujo.edmonds(id_s,id_t)
        A, corte, B = flujo.corte_actual(id_s)
        A  = [grafo.alias(id=a) for a in A]
        A.sort()
        self.assertEqual(A,['c', 's'])

    def test_diapo3_subconjunto_B(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("a","b", 5)
        grafo.insertarArcoConAlias("c","b", 5)
        grafo.insertarArcoConAlias("a","d",10)
        grafo.insertarArcoConAlias("d","c", 2)
        grafo.insertarArcoConAlias("d","e",10)
        grafo.insertarArcoConAlias("c","f", 8)
        grafo.insertarArcoConAlias("f","g", 9)
        grafo.insertarArcoConAlias("s","a", 5)
        grafo.insertarArcoConAlias("s","c",20)
        grafo.insertarArcoConAlias("b","t", 5)
        grafo.insertarArcoConAlias("e","t",10)
        grafo.insertarArcoConAlias("g","t", 8)
        id_s = grafo.idDeNodoAlias("s")
        id_t = grafo.idDeNodoAlias("t")

        flujo = Flujo(grafo)
        fmax = flujo.edmonds(id_s,id_t)
        A, corte, B = flujo.corte_actual(id_s)
        B  = [grafo.alias(id=b) for b in B]
        B.sort()
        self.assertEqual(B,['a','b', 'd','e','f','g','t'])

    def test_diapo3_corte(self):
        grafo = GrafoSimple()
        grafo.insertarArcoConAlias("a","b", 5)
        grafo.insertarArcoConAlias("c","b", 5)
        grafo.insertarArcoConAlias("a","d",10)
        grafo.insertarArcoConAlias("d","c", 2)
        grafo.insertarArcoConAlias("d","e",10)
        grafo.insertarArcoConAlias("c","f", 8)
        grafo.insertarArcoConAlias("f","g", 9)
        grafo.insertarArcoConAlias("s","a", 5)
        grafo.insertarArcoConAlias("s","c",20)
        grafo.insertarArcoConAlias("b","t", 5)
        grafo.insertarArcoConAlias("e","t",10)
        grafo.insertarArcoConAlias("g","t", 8)
        id_s = grafo.idDeNodoAlias("s")
        id_t = grafo.idDeNodoAlias("t")

        flujo = Flujo(grafo)
        fmax = flujo.edmonds(id_s,id_t)
        A, corte, B = flujo.corte_actual(id_s)
        corte  = [(grafo.alias(id=u),grafo.alias(id=v)) for (u,v) in corte]
        corte.sort()
        self.assertEqual(corte,[('c','b'), ('c','f'), ('s', 'a')])


if __name__ == '__main__':
    unittest.main()
