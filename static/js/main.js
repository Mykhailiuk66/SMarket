let avatarInput = document.getElementById("avatar-input")
if (avatarInput) {
  avatarInput.addEventListener("change", (e) => {
    form = document.getElementById("img-form")
    form.submit()
  })
}


const alertElements = document.querySelectorAll('.alert');
alertElements.forEach(alert => {
  setTimeout(() => {
    alert.remove();
  }, 4000);
  alert.addEventListener('click', () => {
    setTimeout(() => {
      alert.remove();
    }, 200);
  });
});


const showPassBtn = document.getElementById('password-toggle-btn')
if (showPassBtn) {
  showPassBtn.addEventListener('click', () => {
    let passInput = document.getElementById("password-toggle");
    if (passInput.type === "password") {
      passInput.type = "text";
    } else {
      passInput.type = "password";
    }
  });
}