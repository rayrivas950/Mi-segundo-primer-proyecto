// cypress/e2e/spec.cy.js

describe('Funcionalidad de Inicio de Sesión', () => {
  // Identificador aleatorio para evitar colisiones en los tests
  const randomId = Math.floor(Math.random() * 1000000);
  const contactName = `Contacto Aleatorio ${randomId}`;
  const contactNotes = `Estas son notas para ${contactName}.`;
  const phone1 = `555-01-${Math.floor(1000 + Math.random() * 9000)}`;
  const phone2 = `555-02-${Math.floor(1000 + Math.random() * 9000)}`;
  const email1 = `email1-${randomId}@test.com`;
  const email2 = `email2-${randomId}@test.com`;

  beforeEach(() => {
    // Visita la página de login antes de cada test
    cy.visit('/login');
  });

  it('debería permitir a un usuario iniciar sesión exitosamente', () => {
    // Introduce el correo electrónico/nombre de usuario y la contraseña
    cy.get('input[type="text"]').type('raynor');
    cy.get('input[type="password"]').type('123456789');

    // Haz clic en el botón de inicio de sesión
    cy.get('button[type="submit"]').click();

    // Afirma que el usuario es redirigido a la página de contactos
    cy.url().should('include', '/contacts');

    // Crear un nuevo contacto
    cy.contains('button', 'Crear Contacto').click();

    // El formulario está en un modal, nos aseguramos de que sea visible
    cy.get('form').contains('Crear Nuevo Contacto').should('be.visible');

    // Rellenar el nombre y las notas
    cy.get('input[placeholder="Nombre del contacto"]').type(contactName);
    cy.get('textarea[placeholder="Notas"]').type(contactNotes);

    // Añadir y rellenar 2 teléfonos (buscamos el botón dentro del grupo de 'Teléfonos')
    cy.contains('h4', 'Teléfonos').parent().find('button').click();
    cy.contains('h4', 'Teléfonos').parent().find('button').click();
    cy.get('input[placeholder="Número de teléfono"]').eq(0).type(phone1);
    cy.get('input[placeholder="Número de teléfono"]').eq(1).type(phone2);

    // Añadir y rellenar 2 emails
    cy.contains('h4', 'Emails').parent().find('button').click();
    cy.contains('h4', 'Emails').parent().find('button').click();
    cy.get('input[placeholder="Correo electrónico"]').eq(0).type(email1);
    cy.get('input[placeholder="Correo electrónico"]').eq(1).type(email2);

    // Guardar el contacto
    cy.get('form').contains('button', 'Crear Contacto').click();

    // Verificar que el nuevo contacto aparece en la lista
    cy.contains('div', contactName).should('be.visible');
    cy.contains('div', phone1).should('be.visible');
    cy.contains('div', email1).should('be.visible');
  });
});