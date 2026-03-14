from typing import List

from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router
import SSS.models as models
import SSS.schemas as schemas

contractor_router = Router()


@contractor_router.get("", response=List[schemas.ContractorResponseSchema])
def get_contractors(request):
    return models.Contractor.objects.all()


@contractor_router.get("/{id}", response=schemas.ContractorResponseSchema)
def get_contractor(request, id: int):
    try:
        return models.Contractor.objects.get(id=id)
    except models.Contractor.DoesNotExist:
        raise Http404


@contractor_router.post("", response=schemas.ContractorResponseSchema)
def create_contractor(request, data: schemas.ContractorRequestSchema):
    contractor = models.Contractor.objects.create(**data.dict())
    return contractor


@contractor_router.put("/{id}", response=schemas.ContractorResponseSchema)
def update_contractor(request, id, data: schemas.ContractorRequestSchema):
    instance = get_object_or_404(models.Equipment, id=id)
    for attr, value in data.dict().items():
        setattr(instance, attr, value)
    instance.save()
    return instance


@contractor_router.delete("/{id}")
def delete_contractor(request, id: int):
    try:
        contractor = models.Contractor.objects.get(id=id)
        contractor.delete()
        return {"success": True}
    except models.Contractor.DoesNotExist:
        raise Http404


equipment_router = Router()


@equipment_router.get("", response=List[schemas.EquipmentResponseSchema])
def get_equipments(request):
    return models.Equipment.objects.all()


@equipment_router.get("/{id}", response=schemas.EquipmentResponseSchema)
def get_equipment(request, id: int):
    equipment = get_object_or_404(models.Equipment, id=id)
    return equipment


@equipment_router.post("", response=schemas.EquipmentResponseSchema)
def create_equipment(request, data: schemas.EquipmentRequestSchema):
    equipment = models.Equipment.objects.create(**data.dict())
    return equipment


@equipment_router.put("/{id}", response=schemas.EquipmentResponseSchema)
def update_equipment(request, id, data: schemas.EquipmentRequestSchema):
    instance = get_object_or_404(models.Equipment, id=id)
    for attr, value in data.dict().items():
        setattr(instance, attr, value)

    instance.save()
    return instance


@equipment_router.delete("/{id}")
def delete_equipment(request, id: int):
    try:
        equipment = models.Equipment.objects.get(id=id)
        equipment.delete()
        return {"success": True}
    except models.Equipment.DoesNotExist:
        raise Http404


object_router = Router()


@object_router.get("", response=List[schemas.ObjectResponseSchema])
def get_objects(request):
    return models.Object.objects.select_related("contractor", "responsible_from_client",
                                                "responsible_from_builder").prefetch_related("equipment").all()


@object_router.get("/{id}", response=schemas.ObjectResponseSchema)
def get_object(request, id: int):
    object = get_object_or_404(models.Object, id=id)
    return object


@object_router.post("", response=schemas.ObjectResponseSchema)
def create_object(request, data: schemas.ObjectRequestSchema):
    object = models.Object.objects.create(**data.dict())
    return object


@object_router.put("/{id}", response=schemas.ObjectResponseSchema)
def update_object(request, id, data: schemas.ObjectRequestSchema):
    instance = get_object_or_404(models.Object, id=id)
    for attr, value in data.dict().items():
        setattr(instance, attr, value)

    instance.save()
    return instance


@object_router.delete("/{id}")
def delete_object(request, id: int):
    try:
        object = models.Object.objects.get(id=id)
        object.delete()
        return {"success": True}
    except models.Object.DoesNotExist:
        raise Http404


object_registration_router = Router()


@object_registration_router.get("", response=List[schemas.ObjectRegistrationResponseSchema])
def get_object_registrations(request):
    return models.ObjectRegistration.objects.select_related("object").all()


@object_registration_router.get("/{id}", response=schemas.ObjectRegistrationResponseSchema)
def get_object_registration(request, id: int):
    object_registrations = get_object_or_404(models.ObjectRegistration, id=id)
    return object_registrations


@object_registration_router.post("/", response=schemas.ObjectRegistrationResponseSchema)
def create_object_registration(request, data: schemas.ObjectRegistrationRequestSchema):
    object_registrations = models.ObjectRegistration.objects.create(**data.dict())
    return object_registrations


@object_registration_router.put("/{id}", response=schemas.ObjectRegistrationResponseSchema)
def update_object_registration(request, id, data: schemas.ObjectRegistrationRequestSchema):
    instance = get_object_or_404(models.ObjectRegistration, id=id)
    for attr, value in data.dict().items():
        setattr(instance, attr, value)

    instance.save()
    return instance


@object_registration_router.delete("/{id}")
def delete_object_registration(request, id: int):
    try:
        object_registration = models.ObjectRegistration.objects.get(id=id)
        object_registration.delete()
        return {"success": True}
    except models.Object.DoesNotExist:
        raise Http404


document_router = Router()


@document_router.get("", response=List[schemas.DocumentResponseSchema])
def get_documents(request):
    return models.Document.objects.select_related("object").all()


@document_router.get("/{id}", response=schemas.DocumentResponseSchema)
def get_document(request, id: int):
    document = get_object_or_404(models.Document, id=id)
    return document


@document_router.post("", response=schemas.DocumentResponseSchema)
def create_document(request, data: schemas.DocumentRequestSchema):
    document = models.Document.objects.create(**data.dict())
    return document


@document_router.put("/{id}", response=schemas.DocumentResponseSchema)
def update_document(request, id, data: schemas.DocumentRequestSchema):
    instance = get_object_or_404(models.Document, id=id)
    for attr, value in data.dict().items():
        setattr(instance, attr, value)

    instance.save()
    return instance


@document_router.delete("/{id}")
def delete_document(request, id: int):
    try:
        document = models.Document.objects.get(id=id)
        document.delete()
        return {"success": True}
    except models.Object.DoesNotExist:
        raise Http404
