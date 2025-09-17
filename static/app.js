// static/app.js
function openLogin(){
    const modal = document.getElementById('modal');
    const body = document.getElementById('modal-body');
    body.innerHTML = `
      <h3>Login</h3>
      <form id="login-form" onsubmit="doLogin(event)">
        <input name="email" placeholder="Email" required/>
        <input name="password" placeholder="Password" type="password" required/>
        <button>Login</button>
      </form>
      <hr/>
      <h4>Or Sign up</h4>
      <form id="signup-form" onsubmit="doSignup(event)">
        <input name="name" placeholder="Name" required/>
        <input name="email" placeholder="Email" required/>
        <input name="password" placeholder="Password" type="password" required/>
        <select name="role"><option>consumer</option><option>business</option><option>farmer</option></select>
        <button>Sign up</button>
      </form>
    `;
    modal.classList.remove('hidden');
  }
  function closeModal(){ document.getElementById('modal').classList.add('hidden'); }
  
  async function doLogin(e){
    e.preventDefault();
    const form = e.target;
    const data = Object.fromEntries(new FormData(form).entries());
    const res = await fetch('/api/login',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)});
    const j = await res.json();
    if(j.status === 'ok'){ alert('Logged in (demo).'); closeModal(); location.href='/dashboard'; }
    else alert('Login failed: ' + (j.message || ''));
  }
  
  async function doSignup(e){
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    const res = await fetch('/api/signup',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)});
    const j = await res.json();
    if(j.status==='ok'){ alert('Signed up!'); closeModal(); location.href='/dashboard'; }
    else alert('Signup failed: ' + (j.message || ''));
  }
  