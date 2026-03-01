from commons.dtos import CreateContactDTO, UpdateContactDTO, ContactDTO
from commons.models import Contact


class ContactRepository:

    def create_contact(self, dto: CreateContactDTO) -> ContactDTO:
        contact = Contact.objects.create(
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
        return self._model_to_dto(contact)

    def get_contact_id(self, contact_id):
        return Contact.objects.get(contact_id=contact_id).contact_id

    def get_contact_first_name(self, contact_id):
        return Contact.objects.get(contact_id=contact_id).first_name

    def delete_contact(self, contact_id):
        contact = Contact.objects.get(contact_id=contact_id)
        contact.delete()
        return True

    def get_all_contacts(self):
        contacts = Contact.objects.all().order_by('last_name')
        return [self._model_to_dto(contact) for contact in contacts]

    def get_contact_by_id(self, contact_id) -> ContactDTO:
        contact = Contact.objects.get(contact_id=contact_id)
        return self._model_to_dto(contact)

    def update_contact(self, contact_id, dto: UpdateContactDTO) -> ContactDTO:
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
        return self._model_to_dto(contact)

    def _model_to_dto(self, contact: Contact) -> ContactDTO:
        return ContactDTO(
            contact_id=contact.contact_id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            type=contact.type,
            siret=contact.siret,
            address=contact.address,
            city=contact.city,
            state=contact.state,
            zip_code=contact.zip_code
        )
