import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPP = ROOT / "cpp" / "hospital_management.cpp"
APP = ROOT / "app.py"
SCREENSHOTS = ROOT / "screenshots"


def test_cpp_contains_required_dsa_operations():
    code = CPP.read_text(encoding="utf-8")
    assert "class Node" in code
    assert "class LinkedList" in code
    assert "Node* next" in code
    assert "void addPatient" in code
    assert "void deletePatient" in code
    assert "while (temp)" in code
    assert "delete temp" in code
    assert "class DoctorList" in code
    assert "class BedManager" in code


def test_streamlit_app_contains_linked_list_implementation():
    code = APP.read_text(encoding="utf-8")
    assert "class PatientNode" in code
    assert "class PatientLinkedList" in code
    assert "class DoctorNode" in code
    assert "class DoctorList" in code
    assert "class BedManager" in code
    assert "contains_id" in code
    compile(code, str(APP), "exec")


def test_expected_screenshots_are_valid_png_files():
    expected = {
        "add_patient.png",
        "admit_patient_dropdown.png",
        "bed_management.png",
        "dashboard_overview.png",
        "delete_patient.png",
        "doctors_registry.png",
        "patient_database.png",
    }
    assert {path.name for path in SCREENSHOTS.glob("*.png")} == expected
    for path in SCREENSHOTS.glob("*.png"):
        with path.open("rb") as file:
            assert file.read(8) == b"\x89PNG\r\n\x1a\n"
            assert file.read(4) == b"\x00\x00\x00\r"
            assert file.read(4) == b"IHDR"
            width, height = struct.unpack(">II", file.read(8))
        assert width >= 1900
        assert height >= 1000


def test_private_reports_and_build_artifacts_are_excluded():
    tracked_names = {path.name.lower() for path in ROOT.rglob("*") if path.is_file()}
    assert "hospital_management.exe" not in tracked_names
    assert not any(name.endswith((".docx", ".pdf")) for name in tracked_names)
