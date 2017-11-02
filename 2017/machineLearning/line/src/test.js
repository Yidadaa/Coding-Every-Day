import { Segment } from './main';

const test = () => {
  const line1 = new Segment({
    startPoint: {
      x: 0,
      y: -1
    },
    endPoint: {
      x: 1,
      y: 0
    }
  });
  const line2 = new Segment({
    startPoint: {
      x: 0,
      y: 1
    },
    endPoint: {
      x: 1,
      y: 0
    }
  });
  console.log(line1, line2, line1.getCorWith(line2));
}
