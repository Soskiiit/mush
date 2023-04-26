let xhr = new XMLHttpRequest();
let method = 'GET';
xhr.onload = function() {
    if (xhr.status == 200) {
        if (xhr.response != loaded_at) {
            location.reload();
        }
        else {
            console.log('actual');
        }
    }
}

function check_updates_loop() {
    for (let i = 0; i < 1000; i++) {
        setInterval(function(){xhr.open(method, url); xhr.send();}, 2000);
    }
}

check_updates_loop();