import api from './api';

const getContacts = (search = '') => {
  return api.get(`/contactos/?search=${search}`);
};

const createContact = (contactData) => {
  return api.post('/contactos/', contactData);
};

const updateContact = (id, contactData) => {
  return api.put(`/contactos/${id}`, contactData);
};

const deleteContact = (id) => {
  return api.delete(`/contactos/${id}`);
};

const contactService = {
  getContacts,
  createContact,
  updateContact,
  deleteContact,
};

export default contactService;
