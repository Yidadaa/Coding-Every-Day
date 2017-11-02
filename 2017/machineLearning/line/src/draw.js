/**
 * @file 负责绘制图形
 */

const c = document.querySelector('#draw');
const text = document.querySelector('#text');
const ctx = c.getContext('2d');
const defaultLineColor = 'black';
const colorSet = colors(6);
ctx.globalAlpha = 0.8;

const scale = 50;
const offsetX = -500;
const offsetY = -600;

c.onmousemove = e => {
  const pointerPos = {
    x: e.pageX,
    y: e.pageY
  };
  const pos = antiTrans(pointerPos);
  text.innerText = `(${pos.x.toFixed(4)}, ${pos.y.toFixed(4)})`;
}

function colors(n) {
  let colors = [];
  for (var i = 0; i < 6; i++) {
    for (var j = 0; j < 6; j++) {
      const color = 'rgb(' + Math.floor(255 - 255 / n * i) + ',' +
        Math.floor(255 - 255 / n * j) + ',0)';
      colors.push(color);
    }
  }
  return colors;
}

function transform(point) {
  const fx = x => x * scale + offsetX;
  const fy = y => y * scale + offsetY;
  return {
    x: fx(point.x),
    y: fy(point.y)
  };
}

function antiTrans(point) {
  const fx = x => (x - offsetX) / scale;
  const fy = y => (y - offsetY) / scale;
  return {
    x: fx(point.x),
    y: fy(point.y)
  };
}

function drawLine(startPoint, endPoint, color) {
  const tsp = transform(startPoint);
  const tep = transform(endPoint);
  // ctx.lineWidth = 2;
  if (color) ctx.strokeStyle = color;
  else ctx.strokeStyle = defaultLineColor; // 恢复样式
  ctx.moveTo(tsp.x, tsp.y);
  ctx.lineTo(tep.x, tep.y);
  ctx.stroke();
}

function drawPoint(point) {
  const tp = transform(point);
  ctx.fillStyle = 'red';
  ctx.beginPath();
  ctx.arc(tp.x, tp.y, 2, 0, Math.PI * 2);
  ctx.fill();
}

function drawRegion(region, color) {
  region.lines.forEach(function (v) {
    // drawPoint(v.startPoint);
    drawLine(v.startPoint, v.endPoint, color)
  }, this);
}

function drawText(text, pos, offsetY) {
  const tp = transform(pos);
  offsetY = offsetY ? offsetY : 0;
  ctx.font = "12px serif";
  ctx.textAlign = 'center';
  ctx.fillStyle = 'blue';
  ctx.fillText(text, tp.x, tp.y + offsetY);
}

function animateRegion(regions, n = 0, time) {
  if (n >= regions.length) return;
  const center = regions[n].center;
  const area = regions[n].area;
  const perimeter = regions[n].perimeter;
  drawText(area.toFixed(2) + '㎡\n', center);
  drawText(perimeter.toFixed(2) + 'm', center, 15);
  drawRegion(regions[n]);
  setTimeout(function () {
    animateRegion(regions, n + 1);
  }, time);
}

import { Point, Segment, Region } from './Classes';

const { findRegion, findRegions } = require('./utils');

const data = require('./data3');

const walls = data.walls;
let regions = findRegions(walls);
regions = regions.map(v => new Region(v));
animateRegion(regions);