from commons.dtos import CreateContactDTO, UpdateContactDTO
from commons.models import Contact


class ContactRepository:

    def create_contact(self, dto: CreateContactDTO) -> Contact:
        return Contact.objects.create(
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            phone=dto.phone,
            type=dto.type,
            siret=dto.siret,
            address=dto.address,
            city=dto.city,
            state=dto.state,
            zip_code=dto.zip_code
        )

    def get_contact_id(self, contact_id):
        return Contact.objects.get(contact_id=contact_id).contact_id

    def get_contact_first_name(self, contact_id):
        return Contact.objects.get(contact_id=contact_id).first_name

    def delete_contact(self, contact_id):
        contact = Contact.objects.get(contact_id=contact_id)
        contact.delete()
        return True

    def get_all_contacts(self):
        return Contact.objects.all().order_by('last_name')

    def get_contact_by_id(self, contact_id):
        return Contact.objects.get(contact_id=contact_id)

    def update_contact(self,  contact_id,dto: UpdateContactDTO) -> Contact:
        contact = Contact.objects.get(contact_id=contact_id)
        if dto.first_name is not None:
            contact.first_name = dto.first_name
        if dto.last_name is not None:
            contact.last_name = dto.last_name
        if dto.email is not None:
            contact.email = dto.email
        if dto.phone is not None:
            contact.phone = dto.phone
        if dto.type is not None:
            contact.type = dto.type
        if dto.siret is not None:
            contact.siret = dto.siret
        if dto.address is not None:
            contact.address = dto.address
        if dto.city is not None:
            contact.city = dto.city
        if dto.state is not None:
            contact.state = dto.state
        if dto.zip_code is not None:
            contact.zip_code = dto.zip_code
        contact.save()
        return contact
