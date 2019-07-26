$(document).ready(function () {
  $('#membersTable').DataTable();
});

var newMember = document.getElementById('newMemberForm');
var closeModalBtn = document.getElementById('closeModalBtn');

// Close modal
closeModalBtn.addEventListener('click', () => {
  location.reload();
});

newMember.addEventListener('submit', e => {
  e.preventDefault();

  let fname = document.getElementById('fname').value;
  let lname = document.getElementById('lname').value;
  let group_id = document.getElementById('group_id').value;
  let gender = document.getElementById('gender').value;
  let age = document.getElementById('age').value;

  if(!fname || !lname || !group_id || !gender || !age) {
    alert('Please provide all required data!');
    return;
  }

  const memberData = {
    fname,
    lname,
    group_id,
    gender,
    age
  }

  fetch(`${window.origin}/members`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json'
    },
    body: JSON.stringify(memberData)
  })
    .then(res => res.json())
    .then(data => {

      if(data.message) {
        document.getElementById('newMemberForm').reset();
        document.getElementById('alertScs').classList.remove('d-none');
        return;
      } else {
        alert('An error occured');
        return;
      }
    })
});
