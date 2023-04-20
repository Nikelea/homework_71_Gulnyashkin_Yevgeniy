
const base_url = 'http://127.0.0.1:8000/api/v2/';
function onLoad() {
    const buttons = document.querySelectorAll('.like-btn');
    buttons.forEach((button) => {

        button.addEventListener('click', like);
    });
}
window.addEventListener('load', onLoad);






const like = function (e) {
    e.preventDefault();
    const pub_id = this.id
    try {
        $.ajax({
            url: 'http://localhost:8000/api/v2/like/' + pub_id,
            method: 'GET',
            headers: { 'Authorization': 'Token ' + localStorage.getItem('apiToken') },
            contentType: 'application/json',
            success: function (response, status) {
                console.log(response);
                let link = document.getElementById(pub_id);
                let count = document.getElementById('b' + pub_id)

                if (response.result === true) {
                    link.innerHTML = 'Unlike';
                    count.innerHTML = ` | &nbsp; ${response.count} people liked this &nbsp; | &nbsp 
            ${response.comment} сomments&nbsp`
                }
                else {
                    count.innerHTML = ` | &nbsp; ${response.count} people liked this &nbsp; | &nbsp 
            ${response.comment} сomments&nbsp`
                    link.innerHTML = 'Like';
                }

            },
            error: function (response, status) { console.log(response); }
        });


        return
    } catch (response) {
    }
}
