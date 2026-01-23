from commons.repositories.contact_repository import ContactRepository


class ContactService:

    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, contact_id, first_name, last_name, email, phone, type, siret, address, city, state, zip_code):
        return self.repo.create_contact(contact_id, first_name, last_name, email, phone, type, siret, address, city, state, zip_code)
    def delete_contact(self, contact_id):
        return self.repo.delete_contact(contact_id)