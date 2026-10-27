class Node:
    """Representa un nodo del árbol AVL.

    Attributes
    ----------
    key: int | float | str
        Valor almacenado.
    left, right: Node | None
        Hijos izquierdo y derecho.
    height: int
        Altura del sub‑árbol cuyo nodo es raíz.
    """
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Un nodo hoja tiene altura 1

class AVLTree:
    """Árbol AVL con inserción, borrado y búsqueda.

    Todas las operaciones mantienen el factor de balance en [-1, 1].
    """
    def __init__(self):
        self.root = None

    # ---------- Utilidades ----------
    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    # ---------- Rotaciones ----------
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        # Rotación
        x.right = y
        y.left = T2
        # Actualizar alturas
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        # Rotación
        y.left = x
        x.right = T2
        # Actualizar alturas
        self._update_height(x)
        self._update_height(y)
        return y

    # ---------- Inserción ----------
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Duplicados no están permitidos en este ejemplo
            return node
        # Actualizar altura y balancear
        self._update_height(node)
        return self._rebalance(node)

    # ---------- Borrado ----------
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Nodo con un solo hijo o sin hijos
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Nodo con dos hijos: obtener el sucesor in‑order
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        # Actualizar altura y balancear
        self._update_height(node)
        return self._rebalance(node)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # ---------- Búsqueda ----------
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if key == node.key:
            return True
        return self._search(node.left, key) if key < node.key else self._search(node.right, key)

    # ---------- Rebalanceo ----------
    def _rebalance(self, node):
        balance = self._balance_factor(node)
        # Caso Izquierda‑Izquierda
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        # Caso Izquierda‑Derecha
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Caso Derecha‑Derecha
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        # Caso Derecha‑Izquierda
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    # ---------- Traversals (para depuración) ----------
    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, acc):
        if node:
            self._inorder(node.left, acc)
            acc.append(node.key)
            self._inorder(node.right, acc)
        return acc


if __name__ == "__main__":
    import random, time
    avl = AVLTree()
    data = random.sample(range(1, 80000), 1000)  # 64536 claves únicas
    start = time.perf_counter()
    for value in data:
        avl.insert(value)
    insert_time = time.perf_counter() - start
    print(f"Insertado 64536 elementos en {insert_time:.6f}s")
    # Verificar búsqueda
    for _ in range(20):
        key = random.choice(data)
        assert avl.search(key)
    # Borrar algunos valores
    for key in data[:50]:
        avl.delete(key)
    print("In‑order después de borrados:", avl.inorder()[:10], "...")


import matplotlib.pyplot as plt
import numpy as np


nodos = np.array([1024,2048,4096,8192,16284,32268,64536])
# Velocidad simulada (por ejemplo, operaciones por segundo o throughput)
velocidad = np.array([0.008373, 0.018283, 0.029784, 0.056816, 0.158383, 0.311316, 0.855745])

# 2. Crear la figura y el gráfico
plt.figure(figsize=(9, 5))
plt.plot(nodos, velocidad, marker='o', linestyle='-', color='b', linewidth=2, label='Rendimiento')

# 3. Aplicar escala logarítmica al eje X
plt.xscale('log')

# 4. Configurar las etiquetas (ticks) del eje X para que muestren los valores exactos
plt.xticks(nodos, labels=nodos)

# 5. Añadir títulos y etiquetas de los ejes
plt.title('Velocidad de Procesamiento vs. Número de Nodos', fontsize=14, fontweight='bold')
plt.xlabel('Número de Nodos', fontsize=12)
plt.ylabel('Velocidad', fontsize=12)

# 6. Añadir cuadrícula (grid) para facilitar la lectura
plt.grid(True, which="both", linestyle='--', alpha=0.5)

# 7. Mostrar la leyenda y el gráfico
plt.legend()
plt.tight_layout()
plt.show()