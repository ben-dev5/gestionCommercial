from commons.models import Contact

class ContactRepository:
   
    def create_contact(self, contact_id, first_name, last_name, email,
                       phone, type, siret, address, city, state, zip_code):
        return Contact.objects.create(
            contact_id=contact_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            type=type,
            siret=siret,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code
        )

    def get_contact_id(self, contact_id):
        return Contact.objects.get().contact_id
    def get_contact_first_name(self, contact_id):
        return Contact.objects.get().first_name
    def delete_contact(self, contact_id):
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
        return True
