import repo

from commons.repositories.contact_repository import ContactRepository


class ContactService:
    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, contact_id, first_name, last_name, email,
                       phone, type, siret, adress, city, state, zip_code):
        return self.repo.create_contact(
            contact_id=contact_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            type=type,
            siret=siret,
            adress=adress,
            city=city,
            state=state,
            zip_code=zip_code
        )

    def delete_contact(self, contact_id):
        repo.delete_contact(contact_id)