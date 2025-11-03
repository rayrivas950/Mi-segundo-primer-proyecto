// cypress/e2e/registration.cy.js

describe('Flujo de Registro y Creación de Contacto', () => {
  it('debería registrar un nuevo usuario, iniciar sesión y crear un nuevo contacto con datos aleatorios', () => {
    // 1. Generar datos aleatorios para la prueba
    const randomId = Date.now();
    const username = `testuser${randomId}`;
    const password = 'password123';
    const contactName = `Contacto Aleatorio ${randomId}`;
    const contactNotes = `Estas son notas para ${contactName}.`;
    const phone1 = `555-01-${Math.floor(1000 + Math.random() * 9000)}`;
    const phone2 = `555-02-${Math.floor(1000 + Math.random() * 9000)}`;
    const email1 = `email1-${randomId}@test.com`;
    const email2 = `email2-${randomId}@test.com`;

    // 2. Registrar un nuevo usuario
    cy.visit('/register');
    cy.get('input[type="text"]').type(username);
    cy.get('input[type="password"]').type(password);
    cy.get('button[type="submit"]').click();

    // 3. Verificar redirección a login e iniciar sesión
    cy.url().should('include', '/login');
    cy.get('input[type="text"]').type(username);
    cy.get('input[type="password"]').type(password);
    cy.get('button[type="submit"]').click();

    // 4. Verificar redirección a la página de contactos
    cy.url().should('include', '/contacts');
    cy.contains('h2', 'Mis Contactos').should('be.visible');

    // 5. Crear un nuevo contacto
    cy.contains('button', 'Crear Contacto').click();

    // El formulario está en un modal, nos aseguramos de que sea visible
    cy.get('form').contains('Crear Nuevo Contacto').should('be.visible');

    // Rellenar el nombre y las notas
    cy.get('input[placeholder="Nombre del contacto"]').type(contactName);
    cy.get('textarea[placeholder="Notas"]').type(contactNotes);

    // Añadir y rellenar 2 teléfonos
    cy.get('h4:contains("Teléfonos") + button').click();
    cy.get('h4:contains("Teléfonos") + button').click();
    cy.get('input[placeholder="Número de teléfono"]').eq(0).type(phone1);
    cy.get('input[placeholder="Número de teléfono"]').eq(1).type(phone2);

    // Añadir y rellenar 2 emails
    cy.get('h4:contains("Emails") + button').click();
    cy.get('h4:contains("Emails") + button').click();
    cy.get('input[placeholder="Correo electrónico"]').eq(0).type(email1);
    cy.get('input[placeholder="Correo electrónico"]').eq(1).type(email2);

    // Guardar el contacto
    cy.get('form').contains('button', 'Crear Contacto').click();

    // 6. Verificar que el nuevo contacto aparece en la lista
    cy.contains('div', contactName).should('be.visible');
    cy.contains('div', phone1).should('be.visible');
    cy.contains('div', email1).should('be.visible');
  });
});