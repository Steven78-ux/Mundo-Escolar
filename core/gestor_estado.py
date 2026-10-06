"""Singleton de persistencia del progreso por estudiante (JSON)."""



import glob
import json
import os
import re
import time
from .logros_config import LOGROS





def _nombre_archivo_seguro(nombre: str) -> str:

    """Evita caracteres problemáticos en rutas de archivo."""

    limpio = re.sub(r"[^\w\-. ]", "_", nombre.strip(), flags=re.UNICODE)

    return limpio or "Invitado"





class GestorEstado:

    """Persistencia en JSON bajo core/data/usuarios/, reiniciable por jornada/usuario."""

    _instancia = None



    def __new__(cls):

        if cls._instancia is None:

            cls._instancia = super().__new__(cls)

            cls._instancia._ruta_archivo = None

            cls._instancia.datos = None

            cls._instancia.usuario_actual = "Invitado"

            cls._instancia.logros_obtenidos = set()

            cls._instancia._dir_usuarios = os.path.join(

                os.path.dirname(os.path.abspath(__file__)), "data", "usuarios"

            )

            os.makedirs(cls._instancia._dir_usuarios, exist_ok=True)

        return cls._instancia



    def inicializar_usuario(self, nombre_usuario):

        """Crea o carga el estado para el usuario dado."""

        self.usuario_actual = nombre_usuario.strip() or "Invitado"

        clave = _nombre_archivo_seguro(self.usuario_actual)

        self._ruta_archivo = os.path.join(self._dir_usuarios, f"{clave}.json")

        self.datos = self._cargar()

        self.logros_obtenidos = set(self.datos.get("logros_obtenidos", []))



    def reset(self):

        """Reinicia el estado al valor por defecto y lo guarda."""

        self.datos = self._estado_default()

        self.logros_obtenidos = set()

        self.guardar()



    def _estado_default(self):

        return {

            "materias": {

                "Lectura y Escritura": 0.0,

                "Ajedrez": 0.0,

                "Computación": 0.0,

                "Robotica": 0.0,

                "Dibujo": 0.0,

            },

            "logros_obtenidos": [],

            "robotica": {

                "misiones_completadas": 0,

                "monedas": 0,

                "niveles_completados": [],

                "dificultad": "basico",

            },

        }



    def _cargar(self):

        if os.path.exists(self._ruta_archivo):

            try:

                with open(self._ruta_archivo, "r", encoding="utf-8") as f:

                    datos = json.load(f)

                if "logros_obtenidos" not in datos:

                    datos["logros_obtenidos"] = []

                return datos

            except Exception:

                return self._estado_default()

        return self._estado_default()



    def guardar(self):

        if self.datos is not None:

            self.datos["logros_obtenidos"] = list(self.logros_obtenidos)

        try:

            with open(self._ruta_archivo, "w", encoding="utf-8") as f:

                json.dump(self.datos, f, indent=4, ensure_ascii=False)

        except Exception as e:

            print(f"Error al guardar estado: {e}")



    def desbloquear_logro(self, logro_id: str) -> bool:

        """Registra un logro por acción específica. Devuelve True si es nuevo."""

        if logro_id not in self.logros_obtenidos:

            self.logros_obtenidos.add(logro_id)

            self.guardar()

            return True

        return False



    def tiene_logro(self, logro_id: str) -> bool:

        return logro_id in self.logros_obtenidos



    def get_materias(self):

        return self.datos.get("materias", {})



    def actualizar_progreso(self, materia, incremento):

        materias = self.get_materias()

        if materia in materias:

            materias[materia] = min(1.0, materias[materia] + incremento)

            self._sincronizar_logros_porcentaje(materia, materias[materia])

            self.guardar()



    def _sincronizar_logros_porcentaje(self, materia: str, valor: float):
        """Desbloquea logros de porcentaje automáticamente al subir progreso."""
        for logro in LOGROS:
            if logro.get("tipo") == "porcentaje" and logro.get("link") == materia:
                if valor >= logro.get("req", 0):
                    self.desbloquear_logro(logro["id"])



    def _ruta_archivo_control(self) -> str:
        """Ruta del archivo que guarda la fecha de la última limpieza."""
        return os.path.join(self._dir_usuarios, "ultima_limpieza.json")

    def _obtener_fecha_ultima_limpieza(self) -> float:
        """Devuelve el timestamp de la última limpieza, o 0 si no existe."""
        archivo = self._ruta_archivo_control()
        if os.path.exists(archivo):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return float(data.get("ultima_limpieza", 0))
            except Exception:
                return 0.0
        return 0.0

    def _guardar_fecha_limpieza(self) -> None:
        """Guarda el timestamp actual como última limpieza."""
        os.makedirs(self._dir_usuarios, exist_ok=True)
        archivo = self._ruta_archivo_control()
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump({"ultima_limpieza": time.time()}, f, indent=4)
        except Exception:
            pass

    def borrar_todos_los_logros(self) -> int:
        """Borra todos los archivos .json de la carpeta de usuarios, excepto el archivo de control."""
        borrados = 0
        archivos_json = glob.glob(os.path.join(self._dir_usuarios, "*.json"))
        for archivo in archivos_json:
            if os.path.basename(archivo) == os.path.basename(self._ruta_archivo_control()):
                continue
            try:
                os.remove(archivo)
                borrados += 1
            except Exception:
                pass
        return borrados

    def limpiar_si_es_necesario(self) -> bool:
        """Verifica si pasó una semana desde la última limpieza y la ejecuta si es necesario."""
        ultima = self._obtener_fecha_ultima_limpieza()
        ahora = time.time()
        una_semana_en_segundos = 7 * 24 * 60 * 60

        if ultima == 0.0 or (ahora - ultima) >= una_semana_en_segundos:
            borrados = self.borrar_todos_los_logros()
            self._guardar_fecha_limpieza()
            print(f"Limpieza semanal completada. Archivos borrados: {borrados}")
            return True

        dias_restantes = int((una_semana_en_segundos - (ahora - ultima)) / (24 * 60 * 60))
        print(f"Próxima limpieza en {dias_restantes} día(s).")
        return False


    @property

    def dir_usuarios(self):

        """Ruta absoluta de core/data/usuarios (útil para admin y tests)."""

        return self._dir_usuarios
