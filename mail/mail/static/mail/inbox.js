document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients=[], subject='', body='') {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const recipients_field = document.querySelector('#compose-recipients');
  const subject_field = document.querySelector('#compose-subject');
  const body_field = document.querySelector('#compose-body');
  recipients_field.value = '';
  subject_field.value = '';
  body_field.value = ''; 

  for (var i = 0; i < recipients.length; i++) {
      if (i == recipients.length-1)
      {
        recipients_field.value = `${recipients[i]}`;
      }
      else {
        recipients_field.value += `${recipients[i]}, `;
      }
    }

  subject_field.value = subject;
  body_field.value = body;

  const compose_form = document.querySelector('#compose-form');
  compose_form.addEventListener("submit", function(event) {
    event.preventDefault();
    submit_email(recipients_field, subject_field, body_field);
  });
}

function submit_email(recipients_field, subject_field, body_field) {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients_field.value,
      subject: subject_field.value,
      body: body_field.value,
    })
  });
  load_mailbox('sent');
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => render_email_header(email, mailbox));
  });
}

function load_email(email, mailbox) {
  document.querySelector('#email-content-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  //Clear out existing email display
  document.querySelector('#email-content-view').innerHTML = '';

  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`emails/${email.id}`)
  .then(response => response.json())
  .then(render_email_content(email));

  if (mailbox !== 'sent')
  {
    render_archive_button(email);
  }
  render_reply_button(email);
}

function render_email_header(email, mailbox) {
  const emailElement = document.createElement('div');
  const senderElement = document.createElement('p');
  const subjectElement = document.createElement('p');
  const timestampElement = document.createElement('p');

  emailElement.addEventListener('click', () => load_email(email, mailbox));
  if (email.read === true) {
    emailElement.classList.add('bg-secondary');
  }
  emailElement.classList.add('email-header');

  senderElement.innerHTML = '<b>Sender: </b>' + email.sender;
  subjectElement.innerHTML = '<b>Subject: </b>' + email.subject;
  timestampElement.innerHTML = '<b>Send Date: </b>' + email.timestamp;
  emailElement.append(senderElement, subjectElement, timestampElement);
  document.querySelector('#emails-view').append(emailElement);
}

function render_email_content(email) {
  const emailContentView = document.querySelector('#email-content-view');
  emailContentView.innerHTML = ''
  emailContentView.classList.add('email-body');

  const emailContentElement = document.createElement('div');
  const senderElement = document.createElement('p');
  const recipientsElement = document.createElement('p');
  const subjectElement = document.createElement('p');
  const timestampElement = document.createElement('p');
  const bodyElement = document.createElement('p');

  senderElement.innerHTML = '<b>Sender: </b>' + email.sender;
  recipientsElement.innerHTML = '<b>Recipients: </b>' + email.recipients;
  subjectElement.innerHTML = '<b>Subject: </b>' + email.subject;
  timestampElement.innerHTML = '<b>Send Date: </b>' + email.timestamp;
  bodyElement.innerHTML = '<b>Body: </b>' + email.body;

  emailContentView.append(emailContentElement);
  emailContentElement.append(senderElement, recipientsElement, subjectElement, timestampElement, bodyElement);
}

function render_archive_button(email) {
  const archiveButton = document.createElement('button');
  if (email.archived == true) {
    archiveButton.innerHTML = 'Unarchive';
    archiveButton.addEventListener('click', () => unarchive(email));
  }
  else {
    archiveButton.innerHTML = 'Archive';
    archiveButton.addEventListener('click', () => archive(email));
  }
  archiveButton.classList.add('btn', 'btn-warning');

  document.querySelector('#email-content-view').append(archiveButton);
}

function render_reply_button(email) {
  const replyButton = document.createElement('button');
  replyButton.innerHTML = 'Reply';

  recipients = [email.sender];
  if (email.subject.substring(0, 4) !== 'Re: ') {
    subject = `Re: ${email.subject}`;
  }
  else {
    subject = email.subject;
  }
  body = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  replyButton.addEventListener('click', () => compose_email(recipients, subject, body));
  replyButton.classList.add('btn', 'btn-success');

  document.querySelector('#email-content-view').append(replyButton);
}

function archive(email) {
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  });
  load_mailbox('inbox');
}

function unarchive(email) {
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  });
  load_mailbox('inbox');
}