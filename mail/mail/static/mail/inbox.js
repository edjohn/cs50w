document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const recipients_field = document.querySelector('#compose-recipients');
  const subject_field = document.querySelector('#compose-subject');
  const body_field = document.querySelector('#compose-body');
  recipients_field.value = '';
  subject_field.value = '';
  body_field.value = '';

  const compose_form = document.querySelector('#compose-form');
  compose_form.addEventListener("submit", submit_email);
}

function submit_email() {
  const recipients_field = document.querySelector('#compose-recipients');
  const subject_field = document.querySelector('#compose-subject');
  const body_field = document.querySelector('#compose-body');
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients_field.value,
      subject: subject_field.value,
      body: body_field.value,
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}