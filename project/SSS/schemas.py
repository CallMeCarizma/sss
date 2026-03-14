from datetime import date
from typing import List, Optional
from decimal import Decimal
from ninja import ModelSchema, Schema
from SSS.models import Contractor, Equipment, Object, ObjectRegistration, Document


class ContractorRequestSchema(ModelSchema):
    class Meta:
        model = Contractor
        fields = ["type", "name", "phone"]


class ContractorResponseSchema(ModelSchema):
    class Meta:
        model = Contractor
        fields = ["id", "type", "name", "phone"]


class EquipmentRequestSchema(ModelSchema):
    class Meta:
        model = Equipment
        fields = ["type", "name", "verification_date", "passport_scan"]


class EquipmentResponseSchema(ModelSchema):
    class Meta:
        model = Equipment
        fields = ["id", "type", "name", "verification_date", "passport_scan"]


class ObjectRequestSchema(ModelSchema):
    equipment: List[int] = []

    class Meta:
        model = Object
        fields = ["contractor", "is_opo", "address", "responsible_from_client", "responsible_from_builder",
                  "checking_frequency", "equipment"]


class ObjectResponseSchema(ModelSchema):
    equipment: List[EquipmentResponseSchema]
    responsible_from_client: ContractorResponseSchema
    responsible_from_builder: ContractorResponseSchema

    class Meta:
        model = Object
        fields = ["id", "contractor", "is_opo", "address", "responsible_from_client", "responsible_from_builder",
                  "checking_frequency", "equipment"]


class ObjectRegistrationRequestSchema(ModelSchema):
    class Meta:
        model = ObjectRegistration
        fields = ["object", "reg_number", "issued_at", "is_active"]


class ObjectRegistrationResponseSchema(ModelSchema):
    object: ObjectResponseSchema

    class Meta:
        model = ObjectRegistration
        fields = ["id", "object", "reg_number", "issued_at", "is_active"]


class DocumentRequestSchema(ModelSchema):
    class Meta:
        model = Document
        fields = ["object", "type", "number", "monthly", "onetime", "comment", "delivery_method"]


class DocumentResponseSchema(ModelSchema):
    class Meta:
        model = Document
        fields = ["id", "object", "type", "number", "monthly", "onetime", "comment", "delivery_method"]
