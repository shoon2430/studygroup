const set_POST = (data = {}) => {
    const opts = {
        method: 'POST',
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: {
            "Content-Type": "application/json"
        },
        redirect: 'follow'
    };
    return opts;
}

const request_POST = (url, massage, data) => {
    if (confirm(massage)) {
        opts = set_POST(data);

        fetch(url, opts)
            .then(function (response) {

                if (response.redirected) {
                    window.location.href = response.url;
                }
            });
    }
}


const set_GET = (data = {}) => {
    const opts = {
        method: 'GET',
        cache: 'no-cache',
        headers: {
            "Content-Type": "application/json"
        }
    };
    return opts;
}

const request_GET = (url, massage) => {
    if (confirm(massage)) {
        opts = set_GET();
        fetch(url, opts)
            .then(function (response) {
                console.log(response)
                window.location.href = response.url;
            });
    }
}