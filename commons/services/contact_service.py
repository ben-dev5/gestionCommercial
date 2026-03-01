from commons.dtos import CreateContactDTO, UpdateContactDTO, ContactDTO
from commons.repositories.contact_repository import ContactRepository


class ContactService:

    def __init__(self):
        self.repo = ContactRepository()

    def create_contact(self, dto: CreateContactDTO) -> ContactDTO:
        return self.repo.create_contact(dto)

    def delete_contact(self, contact_id):
        return self.repo.delete_contact(contact_id)

    def get_all_contacts(self):
        return self.repo.get_all_contacts()

    def get_contact_by_id(self, contact_id) -> ContactDTO:
        return self.repo.get_contact_by_id(contact_id)

    def update_contact(self, contact_id, dto: UpdateContactDTO) -> ContactDTO:
        return self.repo.update_contact(contact_id, dto)
