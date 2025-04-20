function login() 
{
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    fetch('http://127.0.0.1:5000', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
      console.error(err);
      alert("Error logging in");
    });
}
  
