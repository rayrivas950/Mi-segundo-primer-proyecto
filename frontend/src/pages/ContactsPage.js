import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import contactService from '../services/contactService';
import ContactForm from '../components/ContactForm';

const styles = {
  container: {
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
  },
  searchInput: {
    padding: '8px',
    fontSize: '16px'
  },
  contactsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', // Ancho mínimo mayor
    gap: '20px'
  },
  contactCard: {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '15px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    cursor: 'pointer', // Hace la tarjeta clickable
    transition: 'transform 0.2s',
    '&:hover': {
      transform: 'translateY(-5px)'
    }
  },
  contactImage: {
    width: '100%',
    height: '180px',
    objectFit: 'cover',
    borderRadius: '4px',
    marginBottom: '15px'
  },
  contactName: {
    fontSize: '22px',
    fontWeight: 'bold',
    marginBottom: '10px'
  },
  contactDetails: {
    marginBottom: '10px'
  },
  detailItem: {
    fontSize: '14px',
    color: '#333',
    marginBottom: '5px'
  },
  contactNotes: {
    fontSize: '14px',
    color: '#555',
    flexGrow: 1,
    marginTop: '10px',
    fontStyle: 'italic'
  },
  contactDate: {
    fontSize: '12px',
    color: '#888',
    marginTop: '10px',
    textAlign: 'right'
  },
  button: {
    padding: '10px 15px',
    fontSize: '16px',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '4px'
  },
  // Estilos para el modal
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  },
  modalContent: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    width: '70vw', // 70% del ancho de la ventana
    maxHeight: '90vh',
    overflowY: 'auto',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
    position: 'relative'
  },
  closeButton: {
    position: 'absolute',
    top: '10px',
    right: '10px',
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    color: '#333'
  }
};

function ContactsPage() {
  const navigate = useNavigate();
  const [contacts, setContacts] = useState([]);
  const [search, setSearch] = useState('');
  const [editingContact, setEditingContact] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchContacts = useCallback(async () => {
    try {
      const response = await contactService.getContacts(search);
      setContacts(response.data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
      if (error.response && (error.response.status === 401 || error.response.status === 422)) {
        handleLogout();
      }
    }
  }, [search]);

  useEffect(() => {
    fetchContacts();
  }, [fetchContacts]);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const handleContactSaved = () => {
    setShowForm(false);
    setEditingContact(null);
    fetchContacts();
  };

  const handleDelete = async (contactId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este contacto?')) {
      try {
        await contactService.deleteContact(contactId);
        fetchContacts();
        setShowForm(false); // Cerrar el modal después de eliminar
        setEditingContact(null);
      } catch (error) {
        console.error('Error deleting contact:', error);
      }
    }
  };

  const handleCardClick = (contact) => {
    setEditingContact(contact);
    setShowForm(true);
  };

  const handleCloseModal = () => {
    setShowForm(false);
    setEditingContact(null);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2>Mis Contactos</h2>
        <input 
          type="text"
          placeholder="Buscar..."
          style={styles.searchInput}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <div>
          <button onClick={() => { setEditingContact(null); setShowForm(!showForm); }} style={styles.button}>
            {showForm && !editingContact ? 'Cancelar' : 'Crear Contacto'}
          </button>
          <button onClick={handleLogout} style={{...styles.button, marginLeft: '10px', backgroundColor: '#6c757d'}}>Logout</button>
        </div>
      </div>

      <div style={styles.contactsGrid}>
        {contacts.map(contact => (
          <div key={contact.id} style={styles.contactCard} onClick={() => handleCardClick(contact)}>
            <div>
              {contact.image_url && (
                <img src={contact.image_url} alt={contact.nombre} style={styles.contactImage} />
              )}
              <div style={styles.contactName}>{contact.nombre}</div>
              
              <div style={styles.contactDetails}>
                {contact.telefonos && contact.telefonos.slice(0, 2).map(tel => (
                  <div key={tel.id} style={styles.detailItem}>📞 {tel.telefono}</div>
                ))}
                {contact.emails && contact.emails.slice(0, 1).map(email => (
                  <div key={email.id} style={styles.detailItem}>✉️ {email.email}</div>
                ))}
              </div>

              {contact.notes && (
                <p style={styles.contactNotes}>{contact.notes}</p>
              )}

              {contact.created_at && (
                <p style={styles.contactDate}>Creado: {new Date(contact.created_at).toLocaleDateString()}</p>
              )}
            </div>
            {/* Los botones de acción se mueven al modal */}
          </div>
        ))}
      </div>

      {showForm && (
        <div style={styles.modalOverlay} onClick={handleCloseModal}>
          <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <button onClick={handleCloseModal} style={styles.closeButton}>×</button>
            <ContactForm 
              onContactSaved={handleContactSaved} 
              existingContact={editingContact} 
            />
            {editingContact && (
              <button onClick={() => handleDelete(editingContact.id)} style={{...styles.button, backgroundColor: '#dc3545', color: 'white', marginTop: '20px'}}>Eliminar Contacto</button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ContactsPage;
