const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function () {
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Add rating"))
        .catch(error => alert("Error"))
});