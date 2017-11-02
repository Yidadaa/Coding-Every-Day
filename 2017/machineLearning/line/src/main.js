const data = require('./data3');

const {
  findRegion,
  findRegions
} = require('./utils');

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

function drawRegion(walls, color) {
  walls.forEach(function (v) {
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
  const center = findCenter(regions[n]);
  const {area, perimeter} = computeArea(regions[n]);
  drawText(area.toFixed(2) + '㎡\n', center);
  drawText(perimeter.toFixed(2) + 'm', center, 15);
  drawRegion(regions[n]);
  setTimeout(function () {
    animateRegion(regions, n + 1);
  }, time);
}

/**
 * 取区域内最长边的中点
 * @param {*} params 
 */
function findCenter(region) {
  let semgs = [];
  const N = region.length;
  for (let i = 0; i < parseInt(N / 2); i++) {
    for (let j = i + 1; j < N; j++) {
      // 找出图形内所有线段
      const thisSeg = new Segment({
        startPoint: region[i].startPoint,
        endPoint: region[j].startPoint
      });
      const paralledLines = region.filter(v => thisSeg.isParalledWith(v));
      if (paralledLines.length > 0) {
        // 如果该连线与边线平行，那么跳过
        // console.log('fuck')
        continue;
      }
      semgs.push(thisSeg);
    }
  }
  if (semgs.length === 0) return null;
  // 找出没有与其他地方相交的线段
  semgs = semgs.filter(seg => seg.getCorWithRegion(region).length === 0);
  let maxSemgs = semgs[0];
  let maxRatio = 0;
  // 找出面积周长比最大的线段
  semgs.forEach(v => {
    const absR = range => range[1] - range[0];
    const w = absR(v.xRange);
    const l = absR(v.yRange);
    const ratio = l * w;
    // log(v.startPoint, v.endPoint, ratio);
    // TODO: 判断中心点是否在区域内
    if (ratio > maxRatio && isPointInRegion(v.center(), region)) {
      maxRatio = ratio;
      maxSemgs = v;
    }
  });
  // log(semgs, maxSemgs);
  return maxSemgs.center();
}

/**
 * 线段
 */
export class Segment {
  constructor(line) {
    this.a = 0;
    this.b = 0;
    this.c = 0;
    this.id = line.Id;
    // if (!line.Id) log(line)
    this.xRange = [];
    this.yRange = [];
    this.startPoint = line.startPoint;
    this.endPoint = line.endPoint;
    this.distance = 0;
    this.compouteParams();
  }
  compouteParams() {
    const sp = this.startPoint;
    const ep = this.endPoint;
    this.a = sp.y - ep.y;
    this.b = sp.x - ep.x;
    this.c = sp.x * ep.y - sp.y * ep.x;
    this.distance = Math.sqrt(Math.pow(sp.x - ep.x, 2) + Math.pow(sp.y - ep.y, 2));
    this.xRange = [Math.min(sp.x, ep.x), Math.max(sp.x, ep.x)];
    this.yRange = [Math.min(sp.y, ep.y), Math.max(sp.y, ep.y)];
  }
  /**
   * 获取与另一条线段的交点
   * @param {*} seg 
   */
  getCorWith(seg) {
    // 求与另一线段的交点
    const fixed = n => n.toFixed(4);
    let crosp = {};
    if (this.isParalledWith(seg)) return null; // 无解
    const der = this.a * seg.b - this.b * seg.a;
    crosp.x = (this.b * seg.c - this.c * seg.b) / der;
    crosp.y = (this.a * seg.c - this.c * seg.a) / der;
    // 判断是否在两条线段范围内，如果在，那么就判定为相交
    if (this.isInRange(crosp.x, this.xRange) &&
      this.isInRange(crosp.y, this.yRange) &&
      this.isInRange(crosp.x, seg.xRange) &&
      this.isInRange(crosp.y, seg.yRange)) {
      return {
        x: fixed(crosp.x),
        y: fixed(crosp.y)
      };
    } else {
      // log('no cor');
      return null;
    }
  }
  isInRange(n, range) {
    const fixed = n => n.toFixed(4);
    return fixed(n) <= fixed(range[1]) && fixed(n) >= fixed(range[0]);
  }
  /**
   * 获取线条与区域边界的所有交点，不包括线段的端点
   * @param {*} region 
   */
  getCorWithRegion(region) {
    const _this = this;
    return Array.from( // 去重
      new Set(region.map(v => JSON.stringify(_this.getCorWith(v))))
    ).map(JSON.parse).filter(v => !!v).filter(v => {
      return !isEqual(v, _this.startPoint) && !isEqual(v, _this.endPoint);
    });
  }
  isParalledWith(seg) {
    // 是否平行于某线段
    return Math.abs(this.a * seg.b - this.b * seg.a) < 0.00001;
  }
  /**
   * 取中点
   */
  center () {
    const center = p => {
      return {
        x: (p.startPoint.x + p.endPoint.x) / 2,
        y: (p.startPoint.y + p.endPoint.y) / 2
      };
    };
    return center(this);
  }
}
/**
 * 判断两点是否为同一点
 * @param {*} a 
 * @param {*} b 
 */
const isEqual = (a, b) => {
  const sqrt = Math.sqrt;
  const pow2 = n => Math.pow(n, 2);
  return sqrt(pow2(a.x - b.x) + pow2(a.y - b.y)) < 0.00001;
};

const animatePoints = (points, n) => {
  if (n >= points.length) return;
  setTimeout(function () {
    drawPoint(points[n]);
    animatePoints(points, n + 1);
  }, 500);
}
/**
 * 判断某点是否在区域内
 * @param {*} point 
 * @param {*} region 
 */
const isPointInRegion = (point, region) => {
  // 从该点射出一条射线，判断射线与区域的交点个数，奇数个则在区域内
  const testLine = new Segment({
    startPoint: {
      x: 0,
      y: 0
    },
    endPoint: point
  });
  const cros = testLine.getCorWithRegion(region);
  // cros.forEach(drawPoint);
  return cros.length % 2 === 1;
}

/**
 * 计算区域面积及周长
 * @param {*} region 
 */
const computeArea = (region) => {
  const hasID = region.every(v => !!v.id);
  if (!hasID) throw Error('Some Lines Dont Have a ID!');
  let points = region.map(v => v.startPoint);
  // animatePoints(points, 500);
  const delPointFromPoints = (point, points) => {
    return points.filter(v => !isEqual(v, point));
  }
  const perimeter = region.reduce((pre, v) => pre + v.distance, 0);
  let area = 0;
  const maxRun = 1000;
  let count = 0;
  while (points.length > 2) {
    // 在边界上滑动选取三个点，寻找三角形
    // console.log(area);
    count ++;
    if (count > maxRun) {
      // throw Error('Infinate Loop!');
      break;
    }
    const N = points.length;
    for (let i = 0; i < N; i++) {
      const sp = points[i];
      const cp = points[(i + 1) % N];
      const ep = points[(i + 2) % N];
      const trLine = new Segment({
        startPoint: sp,
        endPoint: ep
      });
      // drawPoint(cp);
      if (trLine.getCorWithRegion(region).length === 0 &&
        isPointInRegion(trLine.center(), region)) {
        // 与区域边界不存在交点，并且中点在区域内
        area += computeTriArea(sp, cp, ep);
        const tmp = points;
        points = delPointFromPoints(cp, points);
        // drawLine(trLine.startPoint, trLine.endPoint);
        break;
      }
    }
  }
  return {
    area, perimeter
  };
}
/**
 * 计算三角形面积
 * @param {*} a 
 * @param {*} b 
 * @param {*} c 
 */
const computeTriArea = (a, b, c) => {
  const distance = (a, b) => {
    return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
  };
  const l1 = distance(a, b);
  const l2 = distance(a, c);
  const l3 = distance(b, c);
  const p = (l1 + l2 + l3) / 2;
  return Math.sqrt(p * (p - l1) * (p - l2) * (p - l3));
}

const log = console.log
const walls = data.walls;
let regions = findRegions(walls);
regions = regions.map(region => {
  // log(region);
  return region.map(v => new Segment(v))
});

animateRegion(regions, 0, 200);


// drawRegion(regions[8]);
// console.log(regions.slice(7, 9));
// console.log(findCenter(regions[0]))

const region = regions[3];
console.log(region);
// const line = new Segment({
//   startPoint: region[0].startPoint,
//   endPoint: region[4].startPoint
// });
// console.log(region[0], line, line.getCorWithRegion(region));
// let cp = findCenter(region)
// drawText(computeArea(region).toFixed(2) + '㎡', findCenter(region))
// drawRegion(region);
// animatePoints(region.map(v => v.startPoint), 500)
// drawText('fuck', cp)
// log(isPointInRegion(cp, region))
// computeArea(region);
// log(computeTriArea({
//   x: 0, y: 0
// }, {
//   x: 1, y: 0
// }, {
//   x: 0, y: 1
// }));

// walls.forEach(v => drawLine(v.startPoint, v.endPoint)) // 画出原始墙壁

log(data);

let doors = data.doors;
let doorLines = [data.editLine];

doors.forEach(v => {
  doorLines = doorLines.concat(v.lines);
});

drawRegion(doorLines);

drawRegion(walls);