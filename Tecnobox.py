from abc import ABC, abstractmethod

# ==========================================
# 1. PRINCIPIO ABIERTO/CERRADO (OCP) E INTERFACES (ISP)
# ==========================================
class IImprimible(ABC):
    @abstractmethod
    def generar_detalle(self) -> str:
        pass


# ==========================================
# 2. CLASE BASE DE PRODUCTO (Abstracción)
# ==========================================
class Producto(IImprimible, ABC):
    def __init__(self, nombre: str, precio_base: float):
        self._nombre = nombre
        self._precio_base = precio_base

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def calcular_precio_final(self) -> float:
        pass


class ProductoFisico(Producto):
    def __init__(self, nombre: str, precio_base: float, costo_envio: float):
        super().__init__(nombre, precio_base)
        self.__costo_envio = costo_envio

    def calcular_precio_final(self) -> float:
        return self._precio_base + self.__costo_envio

    def generar_detalle(self) -> str:
        return f"[Físico] {self._nombre} - Precio Total: ${self.calcular_precio_final()}"


# NUEVA EXTENSIBILIDAD: Agregamos un producto digital sin modificar código existente (OCP)
class LicenciaDigital(Producto):
    def __init__(self, nombre: str, precio_base: float, descuento_cyber: float):
        super().__init__(nombre, precio_base)
        self.__descuento_cyber = descuento_cyber

    def calcular_precio_final(self) -> float:
        return self._precio_base * (1 - self.__descuento_cyber)

    def generar_detalle(self) -> str:
        return f"[Digital] {self._nombre} - Precio con Descuento: ${self.calcular_precio_final()}"


# ==========================================
# 3. CAPA DE PERSISTENCIA DESACOPLADA (DIP)
# ==========================================
class IRepositorioInventario(ABC):
    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        pass


class RepositorioDisco(IRepositorioInventario):
    def guardar(self, producto: Producto) -> None:
        print(f"-> [DAL] Guardando '{producto.nombre}' en base de datos / almacenamiento persistente.")


# ==========================================
# 4. GESTOR DE INVENTARIO REFACTORIZADO (SRP y DIP)
# ==========================================
class GestorInventarioRefactorizado:
    def __init__(self, repositorio: IRepositorioInventario):
        # Inyección de Dependencias (DIP)
        self.__repositorio = repositorio
        self.__catalogo = []

    def agregar_producto(self, producto: Producto):
        self.__catalogo.append(producto)
        self.__repositorio.guardar(producto)

    def mostrar_inventario(self):
        print("\n--- INVENTARIO TECNOBOX ACTUALIZADO ---")
        for item in self.__catalogo:
            print(item.generar_detalle())


# ==========================================
# 5. EJECUCIÓN EN CONSOLA (Demostración)
# ==========================================
if __name__ == "__main__":
    # Inyectamos el repositorio en el gestor
    repo = RepositorioDisco()
    sistema_inventario = GestorInventarioRefactorizado(repo)

    # Creamos productos de diferentes tipos
    teclado = ProductoFisico("Teclado Mecánico RGB", 45000, 3500)
    antivirus = LicenciaDigital("Licencia Antivirus Anual", 20000, 0.15)

    # Agregamos al sistema demostrando extensibilidad y SRP
    sistema_inventario.agregar_producto(teclado)
    sistema_inventario.agregar_producto(antivirus)

    # Mostramos resultados
    sistema_inventario.mostrar_inventario()