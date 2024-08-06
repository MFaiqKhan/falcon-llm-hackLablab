from ..models.patient import Patient
from ..extensions import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def create_patient(patient_data):
    patient = Patient(**patient_data)
    db.session.add(patient)
    try:
        db.session.commit()
        return patient.to_dict()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("A patient with this email already exists")

def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    return patient.to_dict() if patient else None

def update_patient(patient_id, patient_data):
    patient = Patient.query.get(patient_id)
    if not patient:
        return None
    for key, value in patient_data.items():
        setattr(patient, key, value)
    patient.updated_at = datetime.utcnow()
    db.session.commit()
    return patient.to_dict()

def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return False
    db.session.delete(patient)
    db.session.commit()
    return True

def list_patients(page=1, per_page=10):
    patients = Patient.query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': [patient.to_dict() for patient in patients.items],
        'total': patients.total,
        'pages': patients.pages,
        'page': page
    }