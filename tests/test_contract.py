import importlib

import pytest

from core.module_factory import SUBJECTS


@pytest.mark.parametrize("subject_id", list(SUBJECTS.keys()))
def test_modulo_expone_crear_frame(subject_id):
    cfg = SUBJECTS[subject_id]
    try:
        module = importlib.import_module(cfg["import_path"])
    except Exception as exc:
        pytest.fail(
            f"{subject_id} no expone crear_frame: no se pudo importar "
            f"{cfg['import_path']}: {exc}",
            pytrace=False,
        )

    assert hasattr(module, "crear_frame"), (
        f"{subject_id} no expone crear_frame"
    )
    assert callable(module.crear_frame), (
        f"{subject_id} no expone crear_frame"
    )
