export class Point {
  /**
   * 点对象
   * @param {*} p 从json中解析得到的点
   */
  constructor (p) {
    this.x = p.x;
    this.y = p.y;
    this.z = p.z;
    this.id = p.Id;
    this.bulge = p.bulge;
  }
  /**
   * 判断两点是否在同一点
   * @param {*Point} p 
   */
  isEqualTo (p) {
    const sqrt = Math.sqrt;
    const pow2 = n => Math.pow(n, 2);
    return sqrt(pow2(this.x - p.x) + pow2(this.y - p.y)) < 0.00001;
  }
  /**
   * 判断点是否在某区域内
   * @param {*Region} region 
   */
  isInRegion (region) {
    // 判断方法，从原点连线到该点，判断连线与区域边界交点个数
    // 若为奇数个，则点在区域内
    const line = new Segment({
      startPoint: new Point({x: 0, y: 0}),
      endPoint: this
    });
    const crossPoints = line.getCorWithRegion(region);
    return crossPoints.length % 2 === 1;
  }
}

export class Segment {
  /**
   * 线段对象，接收从JSON解析出的线
   * @param {*} l 
   */
  constructor (l) {
    // a, b, c 分别是直线的一般形式的三个参数
    this.a = 0;
    this.b = 0;
    this.c = 0;
    this.id = l.Id;
    this.xRange = []; // 用来指定线段的范围
    this.yRange = [];
    this.startPoint = new Point(l.startPoint); // 线段起点
    this.endPoint = new Point(l.endPoint); // 线段终点
    this.distance = l.distance; // 线段长度
    this.computeParams(); // 计算必要的参数
  }
  /**
   * 计算必要参数
   */
  computeParams () {
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
   * 判断是否与另一条线平行
   * @param {*Segment} seg 
   */
  isParalWith (seg) {
    return Math.abs(this.a * seg.b - this.b * seg.a) < 0.00001;
  }
  /**
   * 计算与另一条线段的交点
   * @param {*Segment} seg 
   */
  getCorWith (seg) {
    const fixed = n => n.toFixed(4);
    const isInRange = (n, range) => fixed(n) <= fixed(range[1])
      && fixed(n) >= fixed(range[0]);
    if (this.isParalWith(seg)) return null; // 无解
    const der = this.a * seg.b - this.b * seg.a;
    const x = (this.b * seg.c - this.c * seg.b) / der;
    const y = (this.a * seg.c - this.c * seg.a) / der;
    // 判断是否在两条线段范围内，如果在，那么就判定为相交
    if (isInRange(x, this.xRange) &&
      isInRange(y, this.yRange) &&
      isInRange(x, seg.xRange) &&
      isInRange(y, seg.yRange)) {
      return new Point({
        x: fixed(x),
        y: fixed(y)
      });
    } else {
      return null; // 交点没有在线段上
    }
  }
  /**
   * 计算线段与区域的交点，交点不包括线段的端点
   * @param {*Region} region 
   */
  getCorWithRegion (region) {
    const _this = this;
    return Array.from( // JSON 序列化是为了去重
      new Set(region.map(v => JSON.stringify(_this.getCorWith(v))))
    ).map(JSON.parse).filter(v => !!v).filter(v => { // 除去线段端点
      return !v.isEqualTo(_this.startPoint) && !v.isEqualTo(_this.endPoint);
    });
  }
  /**
   * 取线段中点
   */
  center () {
    return new Point({
      x: (this.startPoint.x + this.endPoint.x) / 2,
      y: (this.startPoint.y + this.endPoint.y) / 2
    });
  }
}

export class Region {
  /**
   * 一片区域，由一组线段围成
   * @param {*Segment<list>} lines 
   */
  constructor (lines) {
    this.lines = lines;
    this.area = 0;
    this.perimeter = 0;
    this.center = this.findCenter();
    this.computeArea()
  }
  /**
   * 找出区域的视觉中心点
   */
  findCenter () {
    const region = this.lines;
    let innerSegments = []; // 内联切分线段，找出所有两点间连线
    const N = region.length;
    for (let i = 0; i < parseInt(N / 2); i++) {
      for (let j = i + 1; j < N; j++) {
        const seg = new Segment({
          startPoint: region[i].startPoint,
          endPoint: region[j].startPoint
        });
        const paralledLines = region.filter(v => seg.isParalWith(v));
        if (paralledLines.length > 1) {
          continue; // 如果该连线与边线之一平行，那么跳过
        }
        innerSegments.push(seg);
      }
    }
    if (innerSegments.length === 0) return null;
    // 找出没有与边界相交的内联线段
    innerSegments = innerSegments.filter(seg => 
      seg.getCorWithRegion(region).length === 0);
    let maxSegment = innerSegments[0];
    let maxRatio = 0;
    // 找出横跨矩形面积最大的线段
    innerSegments.forEach(v => {
      const absR = range => range[1] - range[0];
      const w = absR(v.xRange);
      const l = absR(v.yRange);
      const ratio = l * w;
      // TODO: 判断中心点是否在区域内
      if (ratio > maxRatio && v.center().isInRegion(region)) {
        maxRatio = ratio;
        maxSegment = v;
      }
    });
    return maxSegment.center();
  }
  /**
   * 计算区域面积
   */
  computeArea () {
    const region = this.lines;
    let points = region.map(v => v.startPoint);
    const delPointFromPoints = (point, points) => {
      return points.filter(v => !point.isEqualTo(v));
    }
    const perimeter = region.reduce((pre, v) => pre + v.distance, 0);
    
    let area = 0; // 下面开始计算面积
    const maxRun = 1000; // 防止死循环
    let count = 0;
    while (points.length > 2) {
      count ++;
      if (count > maxRun) {
        break;
      }
      const N = points.length;
      for (let i = 0; i < N; i++) { // 在边界上滑动选取三个点，寻找三角形
        const sp = points[i];
        const cp = points[(i + 1) % N];
        const ep = points[(i + 2) % N];
        const trLine = new Segment({
          startPoint: sp,
          endPoint: ep
        });
        if (trLine.getCorWithRegion(region).length === 0
          && trLine.center().isInRegion(region)) {
          // 与区域边界不存在交点，并且中点在区域内，则进行消解计算
          area += this.computeTriArea(sp, cp, ep);
          const tmp = points;
          points = delPointFromPoints(cp, points);
          break;
        }
      }
    }
    this.area = area;
    this.perimeter = perimeter;
  }
  /**
   * 计算三角形面积，接收三角形顶点坐标
   * @param {*} a 
   * @param {*} b 
   * @param {*} c 
   */
  computeTriArea (a, b, c) {
    const distance = (a, b) => {
      return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
    };
    const l1 = distance(a, b);
    const l2 = distance(a, c);
    const l3 = distance(b, c);
    const p = (l1 + l2 + l3) / 2;
    return Math.sqrt(p * (p - l1) * (p - l2) * (p - l3));
  }
}