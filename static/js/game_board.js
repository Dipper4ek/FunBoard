// Масив позицій фішки (координати на карті)
const positions = [
  {x: 20,  y: 430}, // 1
  {x: 120, y: 430}, // 2
  {x: 220, y: 430}, // 3
  {x: 320, y: 430}, // 4
  {x: 420, y: 430}, // 5
  {x: 520, y: 430}, // 6
  {x: 620, y: 430}, // 7
  {x: 720, y: 430}, // 8
  {x: 820, y: 430},  // 9
  {x: 820, y: 330},
  {x: 820,  y: 230}, // 1
  {x: 720, y: 230}, // 2
  {x: 620, y: 230}, // 3
  {x: 520, y: 230}, // 4
  {x: 420, y: 230}, // 5
  {x: 320, y: 230}, // 6
  {x: 220, y: 230}, // 7
  {x: 120, y: 230}, // 8
  {x: 20, y: 230},  // 9
  {x: 20, y: 130},
  {x: 20,  y: 30}, // 1
  {x: 120, y: 30}, // 2
  {x: 220, y: 30}, // 3
  {x: 320, y: 30}, // 4
  {x: 420, y: 30}, // 5
  {x: 520, y: 30}, // 26
  {x: 620, y: 30}, // 7
  {x: 720, y: 30}, // 8
  {x: 820, y: 30},  // 9
  {x: 920, y: 30},
];

let positionIndex = 0; // початкова позиція (1)
let isMoving = false;  // щоб не кидати кубик під час руху

window.rollDice = function () {
  if (isMoving) return; // не дозволяємо рух під час руху
  const dice = document.getElementById("dice");
  const finalResult = Math.floor(Math.random() * 6) + 1;
  let count = 0;
  let intervalTime = 50;
  const maxSpins = 20;

  const spinDice = () => {
    const randomFace = Math.floor(Math.random() * 6) + 1;
    dice.src = `/static/images/dice${randomFace}.png`;
    dice.style.transform = `rotate(${Math.random() * 360}deg)`;

    count++;
    if (count < maxSpins) {
      intervalTime += 15;
      setTimeout(spinDice, intervalTime);
    } else {
      setTimeout(() => {
        dice.src = `/static/images/dice${finalResult}.png`;
        dice.style.transform = "rotate(0deg)";
        movePlayer(finalResult);
      }, intervalTime);
    }
  };

  spinDice();
};

// Рух фішки по позиціях
function movePlayer(steps) {
  const player = document.getElementById("player");
  isMoving = true;

  let targetIndex = positionIndex + steps;
  if (targetIndex >= positions.length) targetIndex = positions.length - 1;

  const moveStep = () => {
    if (positionIndex >= targetIndex) {   // спочатку перевірка
        isMoving = false;
        return;
    }

    positionIndex++;                       // потім збільшуємо
    const pos = positions[positionIndex];
    player.style.left = `${pos.x}px`;
    player.style.top = `${pos.y}px`;

    setTimeout(moveStep, 600);
};

  moveStep();
}
