import React, { useState, useEffect } from 'react';
import contactService from '../services/contactService';

const styles = {
  form: { 
    padding: '20px', 
    border: '1px solid #ccc', 
    borderRadius: '8px', 
    marginBottom: '20px' 
  },
  input: { 
    display: 'block', 
    width: 'calc(100% - 20px)', 
    padding: '10px', 
    marginBottom: '10px', 
    borderRadius: '4px', 
    border: '1px solid #ddd' 
  },
  button: { 
    padding: '10px 20px', 
    border: 'none', 
    borderRadius: '4px', 
    backgroundColor: '#007bff', 
    color: 'white', 
    cursor: 'pointer', 
    marginRight: '10px'
  },
  removeButton: {
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    padding: '5px 10px',
    borderRadius: '4px',
    cursor: 'pointer',
    marginLeft: '10px'
  },
  fieldGroup: {
    marginBottom: '15px',
    border: '1px solid #eee',
    padding: '10px',
    borderRadius: '5px'
  },
  fieldGroupHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  }
};

// Helper function for email validation
const isValidEmail = email => {
  // Simplified regex for email validation
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};
// Note: Additional frontend validations can be added as needed

function ContactForm({ onContactSaved, existingContact }) {
  const [nombre, setNombre] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [telefonos, setTelefonos] = useState([]);
  const [emails, setEmails] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (existingContact) {
      setNombre(existingContact.nombre || '');
      setImageUrl(existingContact.image_url || '');
      setNotes(existingContact.notes || '');
      setTelefonos(existingContact.telefonos || []);
      setEmails(existingContact.emails || []);
    } else {
      // Reset form if no contact is being edited
      setNombre('');
      setImageUrl('');
      setNotes('');
      setTelefonos([]);
      setEmails([]);
    }
  }, [existingContact]);

  const handleAddTelefono = () => {
    setTelefonos([...telefonos, { telefono: '' }]);
  };

  const handleRemoveTelefono = (index) => {
    const newTelefonos = [...telefonos];
    newTelefonos.splice(index, 1);
    setTelefonos(newTelefonos);
  };

  const handleTelefonoChange = (index, value) => {
    const newTelefonos = [...telefonos];
    newTelefonos[index].telefono = value;
    setTelefonos(newTelefonos);
  };

  const handleAddEmail = () => {
    setEmails([...emails, { email: '' }]);
  };

  const handleRemoveEmail = (index) => {
    const newEmails = [...emails];
    newEmails.splice(index, 1);
    setEmails(newEmails);
  };

  const handleEmailChange = (index, value) => {
    const newEmails = [...emails];
    newEmails[index].email = value;
    setEmails(newEmails);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    if (!nombre) {
      setError('El nombre es obligatorio.');
      return;
    }

    const contactData = {
      nombre,
      image_url: imageUrl,
      notes,
      // Limpiar los IDs antes de enviar para evitar errores de validación de "Unknown field"
      telefonos: telefonos.map(t => ({ telefono: t.telefono })).filter(t => t.telefono.trim() !== ''),
      emails: emails.map(e => ({ email: e.email })).filter(e => e.email.trim() !== ''),
    };

    // Frontend email validation
    for (const emailObj of contactData.emails) {
      if (!isValidEmail(emailObj.email)) {
        setError(`El email '${emailObj.email}' no tiene un formato válido.`);
        return;
      }
    }

    try {
      if (existingContact) {
        await contactService.updateContact(existingContact.id, contactData);
      } else {
        await contactService.createContact(contactData);
      }
      onContactSaved(); // Notify parent to refresh
    } catch (err) {
      console.error('Error saving contact:', err);
      // Mejorar el manejo de errores para mostrar mensajes específicos del backend
      const extractErrorMessages = (errorData) => {
        if (typeof errorData === 'string') {
          return errorData;
        } else if (Array.isArray(errorData)) {
          return errorData.map(extractErrorMessages).join('; ');
        } else if (typeof errorData === 'object') {
          return Object.values(errorData).map(extractErrorMessages).join('; ');
        }
        return '';
      };

      if (err.response && err.response.data) {
        const extracted = extractErrorMessages(err.response.data);
        setError(`Error de validación: ${extracted || 'Hubo un error al guardar el contacto.'}`);
      } else if (typeof err === 'object') {
        setError(`Error inesperado: ${JSON.stringify(err)}`);
      } else {
        setError('Hubo un error al guardar el contacto.');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h3>{existingContact ? 'Editar Contacto' : 'Crear Nuevo Contacto'}</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="text"
        placeholder="Nombre del contacto"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        style={styles.input}
        maxLength={30} // Validación frontend
      />
      <input
        type="text"
        placeholder="URL de la imagen"
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        style={styles.input}
      />
      <textarea
        placeholder="Notas"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        style={styles.input}
        maxLength={150} // Validación frontend
      />

      {/* Campos de Teléfono */}
      <div style={styles.fieldGroup}>
        <div style={styles.fieldGroupHeader}>
          <h4>Teléfonos</h4>
          <button type="button" onClick={handleAddTelefono} style={styles.button}>+</button>
        </div>
        {telefonos.map((tel, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
            <input
              type="text"
              placeholder="Número de teléfono"
              value={tel.telefono}
              onChange={(e) => handleTelefonoChange(index, e.target.value)}
              style={{ ...styles.input, marginBottom: '0px' }}
            />
            <button type="button" onClick={() => handleRemoveTelefono(index)} style={styles.removeButton}>-</button>
          </div>
        ))}
      </div>

      {/* Campos de Email */}
      <div style={styles.fieldGroup}>
        <div style={styles.fieldGroupHeader}>
          <h4>Emails</h4>
          <button type="button" onClick={handleAddEmail} style={styles.button}>+</button>
        </div>
        {emails.map((email, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
            <input
              type="email"
              placeholder="Correo electrónico"
              value={email.email}
              onChange={(e) => handleEmailChange(index, e.target.value)}
              style={{ ...styles.input, marginBottom: '0px' }}
              maxLength={50} // Validación frontend
            />
            <button type="button" onClick={() => handleRemoveEmail(index)} style={styles.removeButton}>-</button>
          </div>
        ))}
      </div>

      <button type="submit" style={{...styles.button, display: 'block', width: '100%', marginTop: '20px'}}>
        {existingContact ? 'Actualizar Contacto' : 'Crear Contacto'}
      </button>
    </form>
  );
}

export default ContactForm;
