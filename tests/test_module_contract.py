import importlib

from core.module_factory import ModuleFactory


def test_todos_los_modulos_exponen_crear_frame():
    for subject_id, config in ModuleFactory.SUBJECTS.items():
        module = importlib.import_module(config["import_path"])
        create_frame = getattr(module, "crear_frame", None)
        assert callable(create_frame), f"{subject_id} no expone crear_frame"
