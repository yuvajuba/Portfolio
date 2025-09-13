const texts = [
  "I'm Juba Bennour,",
  "A junior bioinformatician,",
  "Welcome to my portfolio!"
];

let count = 0;
let index = 0;
let currentText = "";
let letter = "";
let isDeleting = false;

function type() {
  currentText = texts[count];
  
  if (isDeleting) {
    // delete a letter
    letter = currentText.substring(0, index--);
  } else {
    // add a letter
    letter = currentText.substring(0, index++);
  }

  document.getElementById("typing").textContent = letter;

  let speed = isDeleting ? 50 : 200; // deleting : writing speed respectively in ms

  if (!isDeleting && index === currentText.length) {
    // Pause before delete - in ms
    isDeleting = true;
    speed = 1500;
  } else if (isDeleting && index === 0) {
    // Pause before passing to the next text
    isDeleting = false;
    count = (count + 1) % texts.length;
    speed = 500;
  }

  setTimeout(type, speed);
}

type();
