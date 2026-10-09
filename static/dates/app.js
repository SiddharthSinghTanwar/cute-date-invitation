(() => {
  const noButton = document.getElementById("no-button");
  const message = document.getElementById("no-message");
  if (!noButton) return;

  const dodge = (event) => {
    const parent = noButton.closest(".invite-actions");
    if (!parent) return;
    const bounds = parent.getBoundingClientRect();
    const button = noButton.getBoundingClientRect();
    const maxX = Math.max(0, bounds.width - button.width);
    const maxY = 95;
    // Place the shy button within the action area, away from the pointer.
    const pointerX = event && Number.isFinite(event.clientX) ? event.clientX - bounds.left : bounds.width / 2;
    const pointerY = event && Number.isFinite(event.clientY) ? event.clientY - bounds.top : 20;
    let x = Math.random() * maxX;
    let y = Math.random() * maxY - 25;
    if (Math.abs(x - pointerX) < 90) x = x > bounds.width / 2 ? Math.max(0, x - 100) : Math.min(maxX, x + 100);
    if (Math.abs(y - pointerY) < 40) y += y > 0 ? -50 : 50;
    noButton.style.position = "absolute";
    noButton.style.left = `${Math.max(0, Math.min(maxX, x))}px`;
    noButton.style.top = `${y}px`;
    noButton.style.zIndex = "3";
    if (message) message.textContent = ["hehe, try again 🙈", "nope, too slow 💨", "the yes button is right there 💗", "that button has places to be 🏃‍♀️"][Math.floor(Math.random()*4)];
  };
  noButton.addEventListener("pointerenter", dodge);
  noButton.addEventListener("pointerdown", (e) => { e.preventDefault(); dodge(e); });
  noButton.addEventListener("focus", dodge);
  noButton.addEventListener("click", (e) => { e.preventDefault(); dodge(e); });
})();
