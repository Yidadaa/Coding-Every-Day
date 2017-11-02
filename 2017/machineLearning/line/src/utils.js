const findRegion = walls => {
  const delWall = (walls, wall) => {
    return walls.filter(v => v.Id !== wall.Id);
  };
  const findNextWall = (curWall, walls) => {
    return walls.filter(v => {
      return isEqual(v.startPoint, curWall.endPoint) 
        ||isEqual(v.endPoint, curWall.endPoint) 
        ||isEqual(v.startPoint, curWall.startPoint)
        ||isEqual(v.endPoint, curWall.startPoint);
    })[0];
  };

  const isEqual = (a, b) => {
    const [x, y] = [a, b].map(v => {
      return {
        x: v.x, y: v.y
      };
    });
    return Math.sqrt(Math.pow(x.x - y.x, 2) + Math.pow(x.y - y.y, 2)) < 0.00001;
  }

  let curWall = walls[0]
  let region = [curWall]
  const swapPoint = wall => {
    let tmp = wall.startPoint;
    wall.startPoint = wall.endPoint;
    wall.endPoint = tmp;
    return wall;
  };
  while (true) {
    walls = delWall(walls, curWall)
    let nextWall = findNextWall(curWall, walls);
    if (nextWall) {
      // 根据方向，调整nextWall的头尾点
      // 总共有三种需要交换的情况
      if (isEqual(curWall.endPoint, nextWall.endPoint)) {
        nextWall = swapPoint(nextWall);
      } else if (isEqual(curWall.startPoint, nextWall.startPoint)) {
        curWall = swapPoint(curWall);
        region[region.length - 1] = curWall;
      } else if (isEqual(curWall.startPoint, nextWall.endPoint)) {
        curWall = swapPoint(curWall);
        region[region.length - 1] = curWall;
        nextWall = swapPoint(nextWall);
      }
      region.push(nextWall)
    } else {
      // console.log('no next', curWall, walls.length);
      break;
    };
    if (isEqual(nextWall.endPoint, region[0].startPoint)) {
      // console.log('end');
      // break
    };
    curWall = nextWall;
  }
  return {region, walls};
}

const findRegions = walls => {
  let regions = [];
  while (walls.length > 0) {
    const thisIter = findRegion(walls);
    regions.push(thisIter.region);
    walls = thisIter.walls;
  }
  return regions;
}



module.exports = {
  findRegion,
  findRegions
};