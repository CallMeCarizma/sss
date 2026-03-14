from ninja import NinjaAPI
from SSS.api import contractor_router, equipment_router, object_router, object_registration_router, document_router

api = NinjaAPI()

api.add_router("/contractor", contractor_router)
api.add_router("/equipment", equipment_router)
api.add_router("/object", object_router)
api.add_router("/object_registration", object_registration_router)
api.add_router("/document", document_router)
