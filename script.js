const baseURL = 'https://exceed.superposition.pknn.dev';

let door = $('#switch-id1').prop("checked")
let led = $('#switch-id2').prop("checked")
let buzzer = $('#switch-id3').prop("checked")

// GET
function getData() {
  fetch(baseURL + '/data/groupball')
  .then((res) => res.json())
  .then((data) => {
    for (let key in data) {
      if (data[key]) {
        key = true;
      }
    }
  });
}

// POST
function postData(door, buzzer, led) {
  fetch(baseURL + '/data/groupball', {
    method: 'POST',
    body: JSON.stringify({
      "data" : {
        "door" : door,
        "led" : led,
        "buzzer" : buzzer
      }
    }),
    headers: {
      "Content-Type" : 'application/json'
    }
  }).then((res) => res.json())
    .then((data) => console.log(data))
    .catch((err) => console.log(err));
}

function getDoor() {
  fetch(baseURL + '/data/groupball/door')
  .then((res) => res.json())
  .catch((err) => console.log(err));

  let door = $('#switch-id1').prop("checked")
  if (door) {
    door = true;
  } else {
    door = false;
  }
}

function getLED() {
  fetch(baseURL + '/data/groupball/led')
  .then((res) => res.json())
  .catch((err) => console.log(err));

  let led = $('#switch-id2').prop("checked")
  if (led) {
    led = true;
  } else {
    led = false;
  }
}

function getBuzzer() {
  fetch(baseURL + '/data/groupball/buzzer')
  .then((res) => res.json())
  .catch((err) => console.log(err));

  let buzzer = $('#switch-id3').prop("checked")
  if (buzzer) {
    buzzer = true;
  } else {
    buzzer = false;
  }
}

// PUT
function putDoor() {
  let door = $('#switch-id1').prop("checked")
  fetch(baseURL + '/data/groupball/door', {
    method: 'PUT',
    body: JSON.stringify({
      "value" : door
    }),
    headers: {
      "Content-Type" : 'application/json'
    }
  }).then((res) => res.json())
    //.then((data) => console.log(data))
    .catch((err) => console.log(err));
}

function putLED() {
  let led = $('#switch-id2').prop("checked")
  fetch(baseURL + '/data/groupball/led', {
    method: 'PUT',
    body: JSON.stringify({
      "value" : led
    }),
    headers: {
      "Content-Type" : 'application/json'
    }
  }).then((res) => res.json())
    //.then((data) => console.log(data))
    .catch((err) => console.log(err));
}

function putBuzzer() {
  let buzzer = $('#switch-id3').prop("checked")
  fetch(baseURL + '/data/groupball/buzzer', {
    method: 'PUT',
    body: JSON.stringify({
      "value" : buzzer
    }),
    headers: {
      "Content-Type" : 'application/json'
    }
  }).then((res) => res.json())
    //.then((data) => console.log(data))
    .catch((err) => console.log(err));
}

setInterval(() => {
  let door = $('#switch-id1').prop("checked")
  let led = $('#switch-id2').prop("checked")
  let buzzer = $('#switch-id3').prop("checked")
  getData()
  putDoor()
  putLED()
  putBuzzer()
  postData(door, buzzer, led)
}, 2000)


