$(document).ready(function () {
  $('#meetingsTable').DataTable();
});

var newMeeting = document.getElementById('newMeetingForm');
var closeModalBtn = document.getElementById('closeModalBtn');

// Close modal
closeModalBtn.addEventListener('click', () => {
  location.reload();
});

newMeeting.addEventListener('submit', e => {
  e.preventDefault();

  let groupId = document.getElementById('groupId').value;
  let topic = document.getElementById('topic').value;
  let location = document.getElementById('location').value;
  let dateHeld = document.getElementById('dateHeld').value;

  if(!groupId || !topic || !location || !dateHeld) {
    alert('Please fill all the required fields!');
    return;
  };

  const meetingData = {
    groupId,
    topic,
    location,
    dateHeld
  };

  fetch(`${window.origin}/meetings`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json'
      },
      body: JSON.stringify(meetingData)
    })
    .then(res => res.json())
    .then(data => {

      console.log(data)
      if (data.message) {
        document.getElementById('newMeetingForm').reset();
        document.getElementById('alertScs').classList.remove('d-none');
        return;
      } else {
        alert('An error occured');
        return;
      }
    })
});
