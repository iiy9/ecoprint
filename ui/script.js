let currentHue = 0.16;

function setHue(hue, el) {
  currentHue = hue;
  const buttons = document.querySelectorAll('.profile-btn');
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove('active');
  }
  el.classList.add('active');
}

function updateFileName(name) {
  const el = document.getElementById('file-name');
  el.innerText = name;
  el.style.color = 'inherit';
}

function updateProgress(percent, msg) {
  document.getElementById('footer').classList.add('active');
  document.getElementById('progress-bar').style.width = percent + '%';
  document.getElementById('status').innerText = msg;
}

function run() {
  const btn = document.getElementById('run-btn');
  btn.disabled = true;
  btn.innerText = 'WORKING';
  window.pywebview.api.run_process(currentHue);
}

function onComplete(msg) {
  const btn = document.getElementById('run-btn');
  btn.disabled = false;
  btn.innerText = 'PROCESS';
  alert(msg);
}

function onError(msg) {
  const btn = document.getElementById('run-btn');
  btn.disabled = false;
  btn.innerText = 'PROCESS';
  alert('ERROR: ' + msg);
}
