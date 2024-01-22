const canvas = document.getElementById('diagramCanvas');
const ctx = canvas.getContext('2d');

// Set up initial variables
let dots = [];
const dotRadius = 10;
const gridSpacing = 50;
const gridColor = 'lightgray';

function renderGrid() {
  // Draw vertical lines
  for (let x = 0; x <= canvas.width; x += gridSpacing) {
    if (x % (gridSpacing * 2) === 0) continue;
    ctx.strokeStyle = gridColor;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.closePath();
    ctx.stroke();
  }
  
  // Draw horizontal lines
  for (let y = 0; y <= canvas.height; y += gridSpacing) {
    if (y % (gridSpacing * 2) === 0) continue;
    ctx.strokeStyle = gridColor;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.closePath();
    ctx.stroke();
  }
}

function addDot(x, y) {
  const newDot = {
    x,
    y,
    radius: dotRadius,
    selected: false
  };
  dots.push(newDot);
}

function updateDotPosition(dot, dx, dy) {
  dot.x += dx;
  dot.y += dy;
}

function renderDot(dot) {
  ctx.fillStyle = dot.selected ? 'red' : 'black';
  ctx.beginPath();
  ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.closePath();
}

function renderDots() {
  dots.forEach((dot) => {
    renderDot(dot);
  });
}

let selectedDotIndex = -1;

function handleMouseMove(e) {
  if (!mouseDown || selectedDotIndex === -1) return;

  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  dots[selectedDotIndex].x = x;
  dots[selectedDotIndex].y = y;

  renderAll();
}

function handleMouseDown(e) {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  dots.some((_dot, idx) => {
    const distSqr = (x - _dot.x) ** 2 + (y - _dot.y) ** 2;
    if (distSqr <= dotRadius ** 2) {
      selectedDotIndex = idx;
      return true;
    }
    return false;
  });

  if (selectedDotIndex !== -1) {
    prevMouseX = x;
    prevMouseY = y;
  } else {
    addDot(x, y);
    selectedDotIndex = dots.length - 1;
  }

  renderAll();
}

let mouseDown = false;
let prevMouseX, prevMouseY;

canvas.addEventListener('mousedown', (e) => {
  mouseDown = true;
  prevMouseX = e.clientX;
  prevMouseY = e.clientY;
  handleMouseDown(e);
});

canvas.addEventListener('mouseup', () => {
  mouseDown = false;
});

canvas.addEventListener('mousemove', (e) => {
  handleMouseMove(e);
});

function renderAll() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  renderGrid();
  renderDots();
}

renderAll();
