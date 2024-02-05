

const URL = "http://127.0.0.1:2024/ajax_messages";

function sendRequest(method, url, body = null){
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();

    xhr.open(method, url);
    
    xhr.responseType = 'json';
    xhr.setRequestHeader("Content-type", "application/json");
    
    xhr.onload = () => {
      resolve(xhr.response);
    }
    
    xhr.onerror = () => {
      resolve(xhr.response);
    };
    
    xhr.send(JSON.stringify(body));
  })
}

// sendRequest('GET', URL)
// .then(data => console.log(data.messages))
// .catch(err => console.error(err));

const data = {
  message: "Hello, Ajax!",
  user_id: 2
}

sendRequest('POST', URL, data)
  .then(data => console.log(data))
  .catch(err => console.error(err))

/*
style="
              background-image: url(https://image.flaticon.com/icons/svg/145/145867.svg);
            "
*/