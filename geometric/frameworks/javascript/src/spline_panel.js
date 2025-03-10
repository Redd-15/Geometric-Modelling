const POINT_RADIUS = 10;

/**
 * A panel for drawing splines.
 */
class SplinePanel extends Panel
{
  /**
   * Construct a new spline panel.
   */
  constructor(mock)
  {
    super();
    this._points = [
      {x: 200, y: 200},
      {x: 400, y: 200},
      {x: 200, y: 400},
      {x: 400, y: 400},
    ];
    this._tangents = [
      { x: (this._points[1].x - this._points[0].x) * 2, y: (this._points[1].y - this._points[0].y) * 2 },
      { x: (this._points[3].x - this._points[2].x) * 2, y: (this._points[3].y - this._points[2].y) * 2 }
    ];

    this._int_points = [];
    this._selectedPoint = null;
  }

  

  /**
   * Handle the mouse down event.
   */
  onMouseDown(mouse)
  {
    console.log("Mouse down");
    console.log(mouse);
    this._selectedPoint = this.findPoint(mouse.x, mouse.y);
  }

  /**
  * Handle the mouse move event.
  */
  onMouseMove(mouse)
  {
    console.log("Mouse move");
    console.log(mouse);
    if (this._selectedPoint != null) {
      this._selectedPoint.x = mouse.x;
      this._selectedPoint.y = mouse.y;
    }
    this.calcTangents(this._points);
    this.requireRedraw();
  }

  /**
   * Handle the mouse up event.
   */
  onMouseUp(mouse)
  {
    console.log("Mouse up");
    console.log(mouse);
    this._selectedPoint = null;

  }

  /**
   * Handle the key down event.
   */
  onKeyDown(key)
  {
    console.log("Key down");
    console.log(key);
  }

  /**
   * Handle the key up event.
   */
  onKeyUp(key)
  {
    console.log("Key up");
    console.log(key);
  }

  /**
   * Find a control point at the given coordinates.
   */
  findPoint(x, y)
  {
    for (var point of this._points) {
      const dx = point.x - x;
      const dy = point.y - y;
      let distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < POINT_RADIUS) {
        return point;
      }
    }
    return null;
  }

  /**
   * Draw the content of the panel.
   */
  draw(context)
  {
    context.fillStyle = "#FFF";
    context.fillRect(0, 0, this.width, this.height);
    this.drawPoints(context);
    context.strokeStyle = "#AAA";
    this.drawHermite(context, this._points[0], this._points[1], this._tangents[0], this._tangents[0]);
    this.drawHermite(context, this._points[1], this._points[2], this._tangents[0], this._tangents[1]);
    this.drawHermite(context, this._points[2], this._points[3], this._tangents[1], this._tangents[1]);

    //context.stroke();
  }

  /**
   * Draw the control points.
   */
  drawPoints(context)
  {
    for (const point of this._points) {
      this.drawPoint(context, point);
    }
  }

  /**
   * Draw a control point.
   */
  drawPoint(context, point)
  {
    context.strokeStyle = "#00F";
    context.beginPath();
    context.moveTo(point.x - POINT_RADIUS, point.y);
    context.lineTo(point.x + POINT_RADIUS, point.y);
    context.stroke()
    context.beginPath();
    context.moveTo(point.x, point.y - POINT_RADIUS);
    context.lineTo(point.x, point.y + POINT_RADIUS);
    context.stroke()
  }

  /*
  Calculate interpolated points
  */

  calcTangents(_points){
    this._tangents = [
      { x: (_points[1].x - _points[0].x) * 2, y: (_points[1].y - _points[0].y) * 2 },
      { x: (_points[3].x - _points[2].x) * 2, y: (_points[3].y - _points[2].y) * 2 }
    ];
  }
  
  // Hermite interpolation function
  calcHermite(t, P0, P1, T0, T1) {
    const h0 = 2 * t ** 3 - 3 * t ** 2 + 1;
    const h1 = t ** 3 - 2 * t ** 2 + t;
    const h2 = -2 * t ** 3 + 3 * t ** 2;
    const h3 = t ** 3 - t ** 2;
  
    const x = h0 * P0.x + h1 * T0.x + h2 * P1.x + h3 * T1.x;
    const y = h0 * P0.y + h1 * T0.y + h2 * P1.y + h3 * T1.y;
  
    return { x, y };
  }

  drawHermite(context, P0, P1, T0, T1) {
    context.beginPath();
    context.moveTo(P0.x, P0.y);
  
    for (let t = 0; t <= 1; t += 0.001) {
      const pt = this.calcHermite(t, P0, P1, T0, T1);
      context.lineTo(pt.x, pt.y);
    }
  
    context.stroke();
  }
 
}

