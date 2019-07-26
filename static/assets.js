$(document).ready(function () {
  $('#equipmentTable').DataTable();
});

var addEquipment = document.getElementById('equipmentAdd');
var closeModalBtn = document.getElementById('closeModalBtn');

// Close modal
closeModalBtn.addEventListener('click', () => {
  location.reload();
});

// Add New Equipmeent function
addEquipment.addEventListener('submit', e => {
  e.preventDefault();

  let name = document.getElementById('name').value;
  let cost = document.getElementById('cost').value;
  let category = document.getElementById('category').value;
  let quantity = document.getElementById('quantity').value;
  let description = document.getElementById('description').value;

  if (!name || !cost || !category || !quantity || !description) {
    alert('Alert!');
  };

  const postData = {
    name,
    cost,
    category,
    quantity,
    description
  }

  fetch(`${window.origin}/add`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json'
      },
      body: JSON.stringify(postData)
    })
    .then(res => res.json())
    .then(data => {

      if (data.message) {
        document.getElementById('equipmentAdd').reset();
        document.getElementById('alertScs').classList.remove('d-none');
        return;
      } else {
        alert('An error occured');
        return;
      }
    });

});
