document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.edit-button');
    const editModal = document.getElementById('edit-modal');
    const closeModal = document.querySelector('.close');
    const editForm = document.getElementById('edit-form');
    let currentReservationId;

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            currentReservationId = this.getAttribute('data-reservation-id');
            const row = this.closest('tr');
            const programName = row.cells[0].innerText;
            const numOfPeople = row.cells[1].innerText;
            const reservedTime = row.cells[2].innerText;

            document.getElementById('program_name').value = programName;
            document.getElementById('num_of_people').value = numOfPeople;
            document.getElementById('reserved_time').value = reservedTime;

            editModal.style.display = 'block';
        });
    });

    closeModal.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }
    });

    editForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const programName = document.getElementById('program_name').value;
        const numOfPeople = document.getElementById('num_of_people').value;
        const reservedTime = document.getElementById('reserved_time').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        console.log("Submitting edit form");
        console.log(`Reservation ID: ${currentReservationId}`);
        console.log(`Program Name: ${programName}`);
        console.log(`Number of People: ${numOfPeople}`);
        console.log(`Reserved Time: ${reservedTime}`);

        fetch(`/booth_program/edit_reservation/${currentReservationId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({
                'program_name': programName,
                'num_of_people': numOfPeople,
                'reserved_time': reservedTime
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('예약 수정 완료');
                location.reload();
            } else {
                console.log(data);
                alert('예약 수정 실패');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
