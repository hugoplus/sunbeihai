function onSubscribe(event) {
    event.preventDefault();

    let email = document.forms["formSubscription"]["subscriber"].value;

    const csrftoken = Cookies.get('csrftoken');

    const xhttp = new XMLHttpRequest();

    xhttp.onload = function() {
        const resJSON = JSON.parse(this.responseText);

        // Pop up a model dialog to inform the user
        const modalAlert = document.createElement("div");

        modalAlert.setAttribute("class", "modal fade p-4 py-md-5");
        modalAlert.setAttribute("id", "modalAlert");
        modalAlert.setAttribute("data-bs-backdrop", "static");
        modalAlert.setAttribute("data-bs-keyboard", "false");
        modalAlert.setAttribute("tabindex", "-1");
        modalAlert.setAttribute("role", "dialog");
        modalAlert.setAttribute("style", "display:none;");

        modalAlert.innerHTML = `
            <div class="modal-dialog" role="document">
                <div class="modal-content rounded-4 shadow">
                    <div class="modal-header border-bottom-0 bg-success-subtle text-emphasis-success" id="modalHeader">
                        <h1 class="modal-title fs-5" id="modalTitle"></h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body my-3" id="modalBody"></div>
                </div>
            </div>
        `;

        document.body.appendChild(modalAlert);

        if (resJSON["status"] === "success") {
            document.getElementById("modalHeader").setAttribute("class", "modal-header border-bottom-0 bg-success-subtle text-emphasis-success");
        } else {
            document.getElementById("modalHeader").setAttribute("class", "modal-header border-bottom-0 bg-danger-subtle text-emphasis-danger");
        }

        document.getElementById("modalTitle").innerHTML = resJSON["title"];
        document.getElementById("modalBody").innerHTML = "<p>" + resJSON["message"] + "</p>";

        document.getElementById("modalAlert").style.display = "";

        const myModal = new bootstrap.Modal(document.getElementById('modalAlert'), {backdrop: "static"});
        myModal.show();
    };

    xhttp.open("POST", "/course/subscribe/");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send("subscriber=" + email);
};

function handleEllipsisClick(ellipsisPageNumber, currentPage, totalPages) {
    // Calculate the new page number based on the ellipsisPageNumber
    var newPageNumber = ellipsisPageNumber;
    
    if (ellipsisPageNumber < currentPage - 1) { // Left side
        newPageNumber = currentPage - 3;
        newPageNumber = newPageNumber < 1 ? 1 : newPageNumber;
    } else { // Right side
        newPageNumber = currentPage + 3;
        newPageNumber = newPageNumber > totalPages ? totalPages : newPageNumber;
    }
    
    // Redirect to the new page
    window.location.href = '?page=' + newPageNumber;
}